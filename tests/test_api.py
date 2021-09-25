import unittest
import requests
import json

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
        self.assertEqual(json.loads(r.content), expected)

    def test_05_get_by_attribute(self):
        r = requests.get(ApiTest.DISCO_URL, json={"genero":"Pop"})
        expected = {'disco':
                        [{'id': 5,
                          'titulo': 'Thriller',
                          'genero': 'Pop',
                          'artista': 'Michael Jackson',
                          'valor': 250.0
                        },
                        { 'id': 6,
                          'titulo': 'Bad',
                          'genero': 'Pop',
                          'artista': 'Michael Jackson',
                          'valor': 314.15}],
                    'mensagem': 'Disco(s) com filtro {\'genero\': \'Pop\'} retornados com sucesso!'}
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json.loads(r.content), expected)

    def test_07_create_fail(self):
        disc_wrong = {
                        "nome": "Disco Teste",
                        "genero": "Folk",
                        "artista": "Artista Teste",
                        "valor": 42.50
                    }
        expected = {
                "disco": {
                    "nome": "Disco Teste",
                    "genero": "Folk",
                    "artista": "Artista Teste",
                    "valor": 42.50
                },
            "mensagem": "Nao foi possivel criar novo disco!"
        }
        r = requests.post(ApiTest.DISCO_URL, json=disc_wrong)
        r_data = json.loads(r.content)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(json.loads(r.content), expected)

    def test_08_get_one_fail(self):
        r = requests.get("{}/{}".format(ApiTest.DISCO_URL, 10))
        r_data = json.loads(r.content)
        expected = {
            "disco": {},
            "mensagem": "Nao foi possivel retornar o disco de id: 10!"
        }
        self.assertEqual(r.status_code, 400)
        self.assertEqual(json.loads(r.content), expected)

    def test_09_get_by_attribute_fail(self):
        r = requests.get(ApiTest.DISCO_URL, json={"teste":"Pop"})
        expected = {
            "disco": {},
            "mensagem": "Nao foi possivel retornar discos com o filtro {\'teste\': \'Pop\'}!"
        }
        self.assertEqual(r.status_code, 400)
        self.assertEqual(json.loads(r.content), expected)

    def test_10_update_fail(self):
        disc_wrong = {
            "nome": "Titulo Alterado"
            }
        expected = {
            "disco": {},
            "mensagem": "Nao foi possivel atualizar disco 7!"
        }
        r = requests.put("{}/{}".format(ApiTest.DISCO_URL, 7), json=disc_wrong)
        r_data = json.loads(r.content)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(json.loads(r.content), expected)

    def test_11_delete_fail(self):
        r = requests.delete("{}/{}".format(ApiTest.DISCO_URL, 150))
        r_data = json.loads(r.content)
        expected = {
            "disco": {},
            "mensagem": "Nao foi possivel deletar o disco 150!"
        }
        self.assertEqual(r.status_code, 400)
        self.assertEqual(json.loads(r.content), expected)

    def test_12_delete(self):
        r = requests.delete("{}/{}".format(ApiTest.DISCO_URL, 7))
        expected = {
            "disco": {
                "id": 7,
                "titulo": "Titulo Alterado",
                "genero": "Folk",
                "artista": "Artista Teste",
                "valor": 42.50
            },
            "mensagem": "Disco 7 deletado com sucesso!"
        }
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json.loads(r.content), expected)