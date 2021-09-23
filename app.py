import json

from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////database.db'
db = SQLAlchemy(app)

class Discos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255))
    genero = db.Column(db.String(255))
    artista = db.Column(db.String(255))
    valor = db.Column(db.Float)

    def to_json(self):
        return {"id": self.id,
                "titulo": self.titulo,
                "genereo": self.genero,
                "artista": self.artista,
                "valor": self.valor}