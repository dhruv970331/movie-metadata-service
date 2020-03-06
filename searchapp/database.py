import os
import json
import requests
from django.conf import settings
from .rules import Merger

class Catalog:
    catalog_path = "movies"

    def __init__(self):
        """
        Populate catalogue
        """
        self._movies = []
        for movie in os.listdir(self.catalog_path):
            with open(os.path.join(self.catalog_path, movie), "r") as f:
                m = json.load(f)
                self._movies.append({k: self._get_append_value(v)
                                     for k, v in m.items()})
                # self._case_in_movies.append({k.lower():self._get_append_value(v) for k,v in m.items()})
        self.key_case = {k.lower(): k for k in self._movies[0]}

    def _get_append_value(self, item):
        if type(item) is list:
            return [self._get_append_value(x) for x in item]
        if type(item) in [str, int]:
            return str(item).lower()
        return item

    def _search_omdb_catalog(self, imdbId):
        response = requests.get(
            "https://www.omdbapi.com/", params={"i": imdbId, "apikey": settings.OMDB_API_KEY})
        movie = json.loads(response.text)
        return movie

    def filter(self, **kwargs):
        """
        filter for keword search, return all movies in catalog if no keywords are provided
        """
        movies = self._movies.copy()
        if not kwargs.keys():
            return movies
        filtered_movies = []
        kv_pairs = {self.key_case.get(k.lower()):v for k,v in kwargs.items()}
        if (set(kv_pairs.keys()).issubset(set(self.key_case.values()))):
            for movie in self._movies:
                for key, value in kv_pairs.items():
                    flag = False
                    value = value.lower()
                    item = movie.get(key)
                    if type(item) is list:
                        if value in [x.lower() for x in item]:
                            flag = True
                    if value == item:
                        flag = True
                    if not flag:
                        break
                if flag:
                    imdb_movie = self._search_omdb_catalog(movie.get('imdbId'))
                    filtered_movies.append(Merger.merge(imdb_movie,movie))
        return filtered_movies

    def search_by_id(self, Id):
        """
        Search local and omdb catalogue for movies by id
        """
        # if id is numeric try to get movie from local catalogue

        if Id.isnumeric():
            movie = list(filter(lambda x: x.get("id") == Id, self._movies))
            if not movie:
                return {"success": False, "Response":"False", "Error": "Incorrect ID."}
            Id = movie[0].get("imdbId")
            # imdb_movie = self._search_omdb_catalog(imdb_id)

        # if id is alphanumeric try get movie from omdb first since movie may not be in local catalogue

        imdb_movie = self._search_omdb_catalog(Id)
        movie = list(filter(lambda x: x.get("imdbId") ==
                            imdb_movie.get('imdbID'), self._movies))
        if imdb_movie.get("Response") == "True":
            return Merger.merge(imdb_movie,movie[0] if movie else {})
        return imdb_movie


class Movies:
    catalog = Catalog()
