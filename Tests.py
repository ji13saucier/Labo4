import unittest
from Server import Database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database()

    def tearDown(self):
        self.db = None

    def test_can_load_tweets(self):
        self.db.save_tweets("test")
        self.assertEqual(self.db.load_tweets(), ['t','e','s','t'])


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


class TestServer(unittest.TestCase):
    pass


class TestTwitterAPI(unittest.TestCase):
    pass
