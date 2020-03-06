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
        expected = {"success": False,
                    "Response": "False", "Error": "Incorrect ID."}
        self.assertEqual(200, response.status_code)
        self.assertEqual(json.loads(response.content), expected)

    def test_wrong_alphanumeric_id(self):
        url = reverse("search_id", args=["tt040179"])
        response = self.client.get(url)
        expected = {"Response": "False", "Error": "Incorrect IMDb ID."}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected, json.loads(response.content))


class KeywordSearchTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url_name = "search_field"

    def test_no_keywords(self):
        url = reverse(self.url_name)
        response = self.client.get(url)
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_content.get("data")), 4)

    def test_title_keyword(self):
        get_parameters = "?title=Sin+city"
        url = reverse(self.url_name)+get_parameters
        response = self.client.get(url)
        expected = {"success": True, "data": [{"Title": "Sin City", "Year": "2005", "Rated": "R", "Released": "01 Apr 2005", "Genre": "Crime, Thriller", "Director": ["Frank Miller", "Robert Rodriguez", "Quentin Tarantino"], "Writer": ["Frank Miller (graphic novels)"], "Actors": ["Jessica Alba", "Devon Aoki", "Alexis Bledel", "Powers Boothe"], "Plot": "A film that explores the dark and miserable town, Basin City, and tells the story of three different people, all caught up in violent corruption.", "Language": "English", "Country": "USA", "Awards": "34 wins & 52 nominations.", "Poster": "https://m.media-amazon.com/images/M/MV5BODZmYjMwNzEtNzVhNC00ZTRmLTk2M2UtNzE1MTQ2ZDAxNjc2XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg", "Ratings": {
            "Source": "Avg. user rating", "Value": "77"}, "Metascore": "74", "imdbRating": "8.0", "imdbVotes": "725,528", "imdbID": "tt0401792", "Type": "movie", "DVD": "16 Aug 2005", "BoxOffice": "N/A", "Production": "Dimension Films", "Website": "N/A", "Response": "True", "duration": "119", "id": "3532674", "imdbId": "tt0401792", "languages": ["de", "en"], "originalLanguage": "en", "productionYear": "2005", "studios": ["studiocanal", "paramount"]}]}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), expected)

    def test_two_keywords(self):
        get_parameters = "?TiTlE=das+DschunGelbuch&ProduCTionYear=1967"
        url = reverse(self.url_name)+get_parameters
        response = self.client.get(url)
        response_content = json.loads(response.content)
        expected = [{'Title': 'The Jungle Book', 'Year': '1967', 'Rated': 'G', 'Released': '18 Oct 1967', 'Genre': 'Animation, Adventure, Family, Musical', 'Director': ['Wolfgang Reitherman', 'James Algar', 'Jack Kinney'], 'Writer': ['Larry Clemmons (story)', 'Ralph Wright (story)', 'Ken Anderson (story)', 'Vance Gerry (story)', 'Rudyard Kipling (inspired by the Mowgli stories)'], 'Actors': ['Phil Harris', 'Sebastian Cabot', 'Bruce Reitherman', 'George Sanders'], 'Plot': 'Bagheera the Panther and Baloo the Bear have a difficult time trying to convince a boy to leave the jungle for human civilization.', 'Language': 'English', 'Country': 'USA', 'Awards': 'Nominated for 1 Oscar. Another 4 wins & 3 nominations.', 'Poster': 'https://m.media-amazon.com/images/M/MV5BMjAwMTExODExNl5BMl5BanBnXkFtZTgwMjM2MDgyMTE@._V1_SX300.jpg', 'Ratings': {
            'Source': 'Avg. user rating', 'Value': '87'}, 'Metascore': '65', 'imdbRating': '7.6', 'imdbVotes': '157,472', 'imdbID': 'tt0061852', 'Type': 'movie', 'DVD': '11 Feb 2014', 'BoxOffice': 'N/A', 'Production': 'Buena Vista Pictures', 'Website': 'N/A', 'Response': 'True', 'duration': '75', 'id': '11528860', 'imdbId': 'tt0061852', 'languages': ['de', 'en'], 'originalLanguage': 'en', 'productionYear': '1967', 'studios': ['disney']}]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_content.get("data")), 1)
        self.assertEqual(response_content.get("data"),expected)

    def test_keyword_in_array(self):
        get_parameters = "?lAnGuAges=en"
        url = reverse(self.url_name)+get_parameters
        response = self.client.get(url)
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_content.get("data")), 4)

    def test_wrong_keyword(self):
        get_parameters = "?titLe=qwqwqwqw"
        url = reverse(self.url_name)+get_parameters
        response = self.client.get(url)
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_content.get("data")), 0)

    def test_wrong_keyword_in_array(self):
        get_parameters = "?LanGuages=qwqwqwqw"
        url = reverse(self.url_name)+get_parameters
        response = self.client.get(url)
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_content.get("data")), 0)