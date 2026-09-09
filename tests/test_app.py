import json
import threading
import unittest
from http.server import HTTPServer
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from app import Handler
from chatbot import answer

class RetrievalTests(unittest.TestCase):
    def test_specific_topic(self):
        self.assertIn("gravity", answer("What is a black hole?")["answer"])
        self.assertTrue(answer("What is a black hole?")["sources"])
    def test_word_boundaries(self):
        self.assertFalse(answer("Tell me about movie starscream")["sources"])
    def test_unknown(self):
        self.assertFalse(answer("Write a cooking recipe")["sources"])
    def test_no_live_claim(self):
        self.assertFalse(answer("What stars can I see tonight?")["sources"])
    def test_hyphenated(self):
        self.assertIn("distance", answer("What is a light-year?")["answer"])
    def test_specific_over_generic(self):
        self.assertIn("Spiral galaxies", answer("Explain spiral galaxy shapes")["answer"])

class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = "http://127.0.0.1:" + str(cls.server.server_port)
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()
    def test_home(self):
        with urlopen(self.url) as response:
            self.assertIn(b"ORBIT", response.read())
    def test_chat(self):
        request = Request(self.url + "/api/chat", data=json.dumps({"question":"What is a galaxy?"}).encode(), headers={"Content-Type":"application/json"})
        with urlopen(request) as response:
            self.assertTrue(json.load(response)["sources"])
    def test_empty_question(self):
        with self.assertRaises(HTTPError) as caught:
            urlopen(Request(self.url + "/api/chat", data=b'{"question":""}'))
        self.assertEqual(caught.exception.code, 400)
    def test_unknown_path(self):
        with self.assertRaises(HTTPError) as caught:
            urlopen(self.url + "/missing")
        self.assertEqual(caught.exception.code, 404)

if __name__ == "__main__":
    unittest.main()
