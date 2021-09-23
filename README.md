# AMBAR API

Uma implementação simples de uma API usando Flask, SQLite para uma loja de discos de vinil. Projeto feito para o processo seletivo da Ambar.

### Para rodar o servidor:
```
python3 -m pip install -r requirements.txt
python3 src/app.py
```

### Para rodar os testes unitários:
```
python3 -m unittest tests/test_api.py
```

---
## Exemplos de Requisições
### Criar disco

```
curl --location --request POST 'http://127.0.0.1:5000/disco' \
--header 'Content-Type: application/json' \
--data-raw '{
    "titulo": "Paranoid",
    "genero": "Metal",
    "artista": "Black Sabbath",
    "valor": 320.00
}'
```

### Retornar todos os discos
```
curl --location --request GET 'http://127.0.0.1:5000/discos'
```

### Retornar um disco por id
```
curl --location --request GET 'http://127.0.0.1:5000/disco/7'
```

### Retornar um disco por atributo
```
curl --location --request GET 'http://127.0.0.1:5000/artista/Black Sabbath'
```

### Atualiza um disco
```
curl --location --request PUT 'http://127.0.0.1:5000/disco/7' \
--header 'Content-Type: application/json' \
--data-raw '{
    "valor": 389.00
}'
```

### Deletar disco
```
curl --location --request DELETE 'http://127.0.0.1:5000/disco/7'
```
