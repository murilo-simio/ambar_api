# AMBAR API

Uma implementação simples de uma API usando Flask, SQLite para uma loja de discos de vinil

### Para rodar o servidor:
```
python3 src/app.py
```

### Para rodar os testes unitários:
```
python3 -m unittest tests/test_api.py
```

### Endpoints
- GET ALL
-- http://127.0.0.1:5000/discos

- GET ONE
-- http://127.0.0.1:5000/<attribute>/<value>