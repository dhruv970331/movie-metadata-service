import json
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient, APITestCase
from django.shortcuts import reverse
# Create your tests here.


class IdSearchTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_numeric_id(self):
        url = reverse("search_id", args=["3532674"])
        response = self.client.get(url)
        expected = {"Title": "Sin City", "Year": "2005", "Rated": "R", "Released": "01 Apr 2005", "Genre": "Crime, Thriller", "Director": ["Frank Miller", "Robert Rodriguez", "Quentin Tarantino"], "Writer": ["Frank Miller (graphic novels)"], "Actors": ["Jessica Alba", "Devon Aoki", "Alexis Bledel", "Powers Boothe"], "Plot": "A film that explores the dark and miserable town, Basin City, and tells the story of three different people, all caught up in violent corruption.", "Language": "English", "Country": "USA", "Awards": "34 wins & 52 nominations.", "Poster": "https://m.media-amazon.com/images/M/MV5BODZmYjMwNzEtNzVhNC00ZTRmLTk2M2UtNzE1MTQ2ZDAxNjc2XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg", "Ratings": {
            "Source": "Avg. user rating", "Value": "77"}, "Metascore": "74", "imdbRating": "8.0", "imdbVotes": "725,528", "imdbID": "tt0401792", "Type": "movie", "DVD": "16 Aug 2005", "BoxOffice": "N/A", "Production": "Dimension Films", "Website": "N/A", "Response": "True", "duration": "119", "id": "3532674", "imdbId": "tt0401792", "languages": ["de", "en"], "originalLanguage": "en", "productionYear": "2005", "studios": ["studiocanal", "paramount"]}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected, json.loads(response.content))

    def test_alphanumeric_id(self):
        url = reverse("search_id", args=["tt0401792"])
        response = self.client.get(url)
        expected = {"Title": "Sin City", "Year": "2005", "Rated": "R", "Released": "01 Apr 2005", "Genre": "Crime, Thriller", "Director": ["Frank Miller", "Robert Rodriguez", "Quentin Tarantino"], "Writer": ["Frank Miller (graphic novels)"], "Actors": ["Jessica Alba", "Devon Aoki", "Alexis Bledel", "Powers Boothe"], "Plot": "A film that explores the dark and miserable town, Basin City, and tells the story of three different people, all caught up in violent corruption.", "Language": "English", "Country": "USA", "Awards": "34 wins & 52 nominations.", "Poster": "https://m.media-amazon.com/images/M/MV5BODZmYjMwNzEtNzVhNC00ZTRmLTk2M2UtNzE1MTQ2ZDAxNjc2XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg", "Ratings": {
            "Source": "Avg. user rating", "Value": "77"}, "Metascore": "74", "imdbRating": "8.0", "imdbVotes": "725,528", "imdbID": "tt0401792", "Type": "movie", "DVD": "16 Aug 2005", "BoxOffice": "N/A", "Production": "Dimension Films", "Website": "N/A", "Response": "True", "duration": "119", "id": "3532674", "imdbId": "tt0401792", "languages": ["de", "en"], "originalLanguage": "en", "productionYear": "2005", "studios": ["studiocanal", "paramount"]}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected, json.loads(response.content))

    def test_wrong_numeric_id(self):
        url = reverse("search_id", args=["0401792"])
        response = self.client.get(url)
        expected = {"success": False, "Response": "False", "Error": "Incorrect ID."}
        self.assertEqual(200,response.status_code)
        self.assertEqual(json.loads(response.content),expected)

    def test_wrong_alphanumeric_id(self):
        url = reverse("search_id", args=["tt040179"])
        response = self.client.get(url)
        expected = {"Response": "False", "Error": "Incorrect IMDb ID."}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected, json.loads(response.content))