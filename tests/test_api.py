import unittest
import requests
import json
from time import sleep

class ApiTest(unittest.TestCase):
    API_URL = "http://127.0.0.1:5000"
    DISCOS_URL = "{}/discos".format(API_URL)
    DISCO_URL = "{}/disco".format(API_URL)
    DISCO_OBJ = {
        "titulo": "Disco Teste",
        "genero": "Folk",
        "artista": "Artista Teste",
        "valor": 42.50
    }
    DISCO_UPD = {
        "titulo": "Titulo Alterado"
    }

    def test_01_get_all(self):
        r = requests.get(ApiTest.DISCOS_URL)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 2)

    def test_02_create_one(self):
        r = requests.post(ApiTest.DISCO_URL, json=ApiTest.DISCO_OBJ)
        self.assertEqual(r.status_code, 201)

    def test_03_update(self):
        r = requests.put("{}/{}".format(ApiTest.DISCO_URL, 7), json=ApiTest.DISCO_UPD)
        self.assertEqual(r.status_code, 200)

    def test_04_get_new(self):
        r = requests.get("{}/{}".format(ApiTest.DISCO_URL, 7))
        r_data = json.loads(r.content)
        expected = {
            "disco": {
                "id": 7,
                "titulo": "Titulo Alterado",
                "genero": "Folk",
                "artista": "Artista Teste",
                "valor": 42.50
            },
            "mensagem": "Disco 7 retornado com sucesso"
        }
        self.assertEqual(r.status_code, 200)
        assert r_data == expected

    def test_05_delete(self):
        sleep(0.05)
        r = requests.delete("{}/{}".format(ApiTest.DISCO_URL, 7))
        self.assertEqual(r.status_code, 200)