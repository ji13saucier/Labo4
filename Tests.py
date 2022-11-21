import unittest
from http.server import SimpleHTTPRequestHandler

import requests

import Server
from Server import Database
from TwitterAPI import TwitterAPI
from Server import Lab4HTTPRequestHandler


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database()

    def tearDown(self):
        self.db = None

    def test_can_load_tweets(self):
        self.db.save_tweets("test")
        self.assertEqual(self.db.load_tweets(), ['t', 'e', 's', 't'])

    def test_no_tweets_stored(self):
        self.assertEqual(self.db.load_tweets(), [])

    def test_can_save_tweets(self):
        self.db.save_tweets("tweet1")
        answer = []
        answer.extend("tweet1")
        self.assertEqual(self.db.tweets, answer)

    def test_cant_save_multiple_tweets(self):
        self.db.save_tweets("tweet2")
        self.db.save_tweets("Essais2")
        answer = []
        answer.extend("Essais2")
        self.assertEqual(self.db.tweets, answer)


# class TestServer(unittest.TestCase):

    # def setUp(self):
    #    self.path = "http://localhost:8080/queryTwitter?query="

    # def tearDown(self):
    #    self.path = None

    # def test_server_queries(self):
    #    Lab4HTTPRequestHandler.path = "/queryTwitter?query=test"
    #    Lab4HTTPRequestHandler.do_GET(Lab4HTTPRequestHandler)
    #    self.assertEqual("Display.html", Lab4HTTPRequestHandler)

    # def test_server_search(self):
    #    Server.Lab4HTTPRequestHandler.path = '/'
    #    Server.Lab4HTTPRequestHandler.do_GET(Server.Lab4HTTPRequestHandler)
    #    self.assertEqual('Search.html', Lab4HTTPRequestHandler.path)


class TestTwitterAPI(unittest.TestCase):
    def test_create_headers(self):
        self.assertIsNotNone(TwitterAPI.create_twitter_headers())

    def test_query_twitter_api(self):

        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url("test")
        json_response = TwitterAPI.query_twitter_api(url, headers, params)

        response = requests.request('GET', url, headers=headers, params=params)
        self.assertIsNotNone(response.json())

    def test_empty_query_twitter_api(self):
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url("")
        json_response = TwitterAPI.query_twitter_api(url, headers, params)

        response = requests.request('GET', url, headers=headers, params=params)
        self.assertIsNotNone(response.json())

    def test_twitter_url_one_word(self):
        self.assertEqual(('https://api.twitter.com/2/tweets/search/recent', {
            'query': "test",
            'max_results': 10,
            'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
            'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,'
                            'public_metrics,referenced_tweets,reply_settings,source',
            'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
            'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
            'next_token': {}
        }), TwitterAPI.create_twitter_url(["Test", "Test2"]))

    def test_twitter_url_multiple_words(self):
        self.assertEqual(('https://api.twitter.com/2/tweets/search/recent', {
            'query': "test for multiples queries",
            'max_results': 10,
            'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
            'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,'
                            'public_metrics,referenced_tweets,reply_settings,source',
            'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
            'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
            'next_token': {}
        }), TwitterAPI.create_twitter_url("test for multiples queries"))

    def test_twitter_base_param(self):
        self.assertEqual(('https://api.twitter.com/2/tweets/search/recent', {
            'query': "test",
            'max_results': 10,
            'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
            'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,'
                            'public_metrics,referenced_tweets,reply_settings,source',
            'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
            'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
            'next_token': {}
        }), TwitterAPI.create_twitter_url("test"))  # laisser aux valeur de max_results par défault

    def test_twitter_custom_param(self):
        self.assertEqual(('https://api.twitter.com/2/tweets/search/recent', {
            'query': "test",
            'max_results': 15,
            'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
            'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,'
                            'public_metrics,referenced_tweets,reply_settings,source',
            'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
            'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
            'next_token': {}
        }), TwitterAPI.create_twitter_url("test", 15))  # max_results modifier à 15

    def test_twitter_weird_character_query(self):
        self.assertEqual(('https://api.twitter.com/2/tweets/search/recent', {
            'query': ",",
            'max_results': 10,
            'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
            'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,'
                            'public_metrics,referenced_tweets,reply_settings,source',
            'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
            'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
            'next_token': {}
        }), TwitterAPI.create_twitter_url(","))

    def test_twitter_none_character_query(self):
        self.assertEqual(('https://api.twitter.com/2/tweets/search/recent', {
            'query': " ",
            'max_results': 10,
            'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
            'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,'
                            'public_metrics,referenced_tweets,reply_settings,source',
            'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
            'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
            'next_token': {}
        }), TwitterAPI.create_twitter_url(None))

    def test_empty_url(self):
        pass
