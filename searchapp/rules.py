#TODO Refactor code
class Merger:
    overwrite = ['title', 'description', 'Runtime']
    transform = ['Director', 'Writer', 'Actors']

    def __init__(self, imdb_movie, movie):
        self.imdb_movie = imdb_movie.copy()
        self.local_movie = movie
        imdb_movie.update(movie)
        self.movie = imdb_movie

    @classmethod
    def merge(cls, imdb_movie, movie):
        if movie:
            merger = cls(imdb_movie, movie)
            return merger.merged_obj
        return imdb_movie

    @property
    def merged_obj(self):
        self._apply_overwrite()
        self._apply_transform()
        self._apply_ratings()
        return self.movie

    def _apply_overwrite(self):
        """
            Remove field as per rules after merging
        """
        for field in self.overwrite:
            if self.movie.get(field):
                self.movie.pop(field)

    def _apply_transform(self):
        """
            Apply transforms to fields: change str fields to arrays as per rules
        """
        for field in self.transform:
            if self.movie.get(field):
                self.movie[field] = [x.strip()
                                     for x in self.movie.get(field).split(',')]

    def _apply_ratings(self):
        """
            Calculate average ratings by multplying star counts with corresponding values of stars and totaling with total number of stars to get average percentage user rating
        """
        ratings = self.movie.get('userrating')
        values = list(ratings.values())[:-1]
        s = sum([int(v)*(i+1) for i, v in enumerate(values)])
        t = sum([int(v)*5 for i, v in enumerate(values)])
        self.movie['Ratings'] = {
            "Source": "Avg. user rating", "Value": str(s*100//t)}
        self.movie.pop("userrating")
