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

    # test_can_load_tweets vérifie que l'on peut sortir les valeurs contenu dans la database. Le code contenait déja la solution.
    def test_can_load_tweets(self):
        self.db.save_tweets("test")
        self.assertEqual(self.db.load_tweets(), ['t', 'e', 's', 't'])

    # test_no_tweets_stored permet de vérifier si il y a des tweets dans la database ou si elle est empty.
    # Lorsqu'elle est vide la database retourne un liste vide
    def test_no_tweets_stored(self):
        self.assertEqual(self.db.load_tweets(), [])

    # test_can_save tweets vérifie que la fonction save_tweets enregistre belle et bien dans la database.
    def test_can_save_tweets(self):
        self.db.save_tweets("tweet1")
        answer = []
        answer.extend("tweet1")
        self.assertEqual(self.db.tweets, answer)

    # test_cant_save_multiple_tweets, il permet vérifier que les ancients tweets ne reste pas dans la database.
    # On a ajouté une section de code qui réinitialise la databases. ceci a pour but d'évité les effets de in and
    # out avec recherche multiple
    def test_cant_save_multiple_tweets(self):
        self.db.save_tweets("tweet2")
        self.db.save_tweets("Essais2")
        answer = []
        answer.extend("Essais2")
        self.assertEqual(self.db.tweets, answer)

class TestServer(unittest.TestCase):

    # Malheureusemenbt l'ensemble de nos TestServer furent des échec. Nous n'avons pas été en mesure de faire
    # fonctionné des test unitaire ici. L'utilisation du SimpleHTTPRequestHandler ne nous permettait pas
    # d'initialisé une classe Lab4HTTPRequestHandler. Notre manque de connaissance flagrant en langage python en est
    # la principale cause
     def setUp(self):
        request = Server.Lab4HTTPRequestHandler(SimpleHTTPRequestHandler).path


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

pass

class TestTwitterAPI(unittest.TestCase):

    # test_create_headers vérifie que la fonction create_twitter_headers() est fonctionnel et non null.
    def test_create_headers(self):
        self.assertIsNotNone(TwitterAPI.create_twitter_headers())

    # test_query_twitter_api verifie la création du Json des tweets recherché et verifie que c'est non-null
    def test_query_twitter_api(self):

        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url("test")
        json_response = TwitterAPI.query_twitter_api(url, headers, params)

        self.assertIsNotNone(json_response)

    # test_empty_query_twitter_api verifie que l'entrée d'une chaine de caractere vide donne un json non-vide
    def test_empty_query_twitter_api(self):
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url("")
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        print(json_response)

        self.assertIsNotNone(json_response)

    # test_none_query_twitter_api verifie si cree le json des tweets est non-nul
    def test_none_query_twitter_api(self):
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url(None)
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        self.assertIsNotNone(json_response)

    # test_find_tweet_from_json test si il est possible de trouver les différents tweets selon les données recherchées
    def test_find_tweet_from_json(self):
        database = Database();
        data = 'salut'
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url(data)
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        tweets = json_response['data']
        self.assertIsNotNone(tweets)

    # test_find_tweet_from_json_none_data test si il est possible de trouvé les différents tweets
    #                                     selon un data Null
    # ce test ne marche pas, on ne comprend pas vraiment comment vraiment faire ce test proprement
    # car ce le data provient normalement de l'entrée de l'utilisateur et sa definition se fait à
    # l'intérieur meme du code.
    def test_find_tweet_from_json_none_data(self):
        data = None
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url(data)
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        tweets = json_response['data']
        self.assertIsNotNone(tweets)

    # test_find_tweet_from_json_empty_data test si il est possible de trouvé les différents tweets
    #                                      selon un data vide.

    # j'ai le meme probleme que pour le test précedent, je ne suis pas sur de savoir comment réelement
    # faire ce test pour que la solution implémenté dans le code corrige réellement le test.
    def test_find_tweet_from_json_empty_data(self):
        data = ''
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url(data)
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        tweets = json_response['data']
        self.assertIsNotNone(tweets)

    # test_find_tweet_from_json_space_data test si il est possible de trouvé les différents tweets
    #                                      selon un espace.
    #
    # j'ai le meme probleme que pour le test précedent, je ne suis pas sur de savoir comment réelement
    # faire ce test pour que la solution implémenté dans le code corrige réellement le test.
    def test_find_tweet_from_json_space_data(self):
        data = ' '
        headers = TwitterAPI.create_twitter_headers()
        url, params = TwitterAPI.create_twitter_url(data)
        json_response = TwitterAPI.query_twitter_api(url, headers, params)
        tweets = json_response['data']
        self.assertIsNotNone(tweets)

    #test_twitter_url_one_word test pour voir si la fonction de créé le url fonctionne avec un
    # seul mot en query
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
        }), TwitterAPI.create_twitter_url("test"))

    # test_twitter_url_multiple_words test pour voir si la fonction de créé le url fonctionne avec
    # plusieurs mots en query
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

    # test_twitter_base_param test pour voir si la fonction créé le url fonctionne avec
    # une quantité de result max de base.
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

    # test_twitter_custom_param test pour voir si la fonction créé le url fonctionne avec
    # une quantité de result max determiné.
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

    # test_twitter_weird_character_query test pour voir si la fonction de créé le url fonctionne avec
    # un caractere spécial dans le query.
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

    # test_twitter_none_character_query test pour voir si la fonction de créé le url fonctionne avec
    # une valeur null dans le query.
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
