import json
import os
from logging import exception

from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy

# Caminho para a pasta atual
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Configura o db
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(BASEDIR,'discos.db')
db = SQLAlchemy(app)

# Tabela Discos
class Discos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255))
    genero = db.Column(db.String(255))
    artista = db.Column(db.String(255))
    valor = db.Column(db.Float)

    # Estrutura o retorno das requisicoes
    def to_json(self):
        return {"id": self.id,
                "titulo": self.titulo,
                "genero": self.genero,
                "artista": self.artista,
                "valor": self.valor}

# Retorna todos os discos
@app.route("/discos", methods=["GET"])
def get_all():
    discs_obj = Discos.query.all()
    discs_json = [disc.to_json() for disc in discs_obj]
    return send_response(status=200,
                         body=discs_json,
                         msg=f"Todos os {len(discs_json)} discos foram retornados com sucesso")

# Retorna apenas um disco
@app.route("/disco/<id>", methods=["GET"])
def get_one(id: int):
    try:
        disc_obj = Discos.query.filter_by(id=id).first()
        disc_json = disc_obj.to_json()
        return send_response(status=200,
                             body=disc_json,
                             msg=f"Disco {id} retornado com sucesso")
    except:
        return send_response(status=400,
                             body={},
                             msg=f"Nao foi possivel retornar o disco de id: {id}!")

# Retorna discos por atributo
@app.route("/disco", methods=["GET"])
def get_by_attribute():
    filtro = request.get_json()
    try:
        discs_obj = Discos.query.filter_by(**filtro)
        disc_json = [disc.to_json() for disc in discs_obj]
        if len(disc_json) < 1:
                raise exception
        return send_response(status=200,
                             body=disc_json,
                             msg=f"Disco(s) com filtro {filtro} retornados com sucesso!")
    except:
        return send_response(status=400,
                             body={},
                             msg=f"Nao foi possivel retornar discos com o filtro {filtro}!")

# Cria um disco novo
@app.route("/disco", methods=["POST"])
def create():
    body = request.get_json()
    try:
        disc = Discos(titulo=body["titulo"],
                      genero=body["genero"],
                      artista=body["artista"],
                      valor=body["valor"])
        db.session.add(disc)
        db.session.commit()
        return send_response(status=201,
                             body=disc.to_json(),
                             msg="Disco Adicionado com sucesso!")
    except:
        return send_response(status=400,
                             body=body,
                             msg="Nao foi possivel criar novo disco!")

# Atualiza um disco
@app.route("/disco/<id>", methods=["PUT"])
def update(id: int):
    disc_obj = Discos.query.filter_by(id=id).first()
    body = request.get_json()
    
    try:
        for key, value in body.items():
            if key not in disc_obj.to_json():
                raise exception
            setattr(disc_obj, key, value)
        db.session.commit()
        return send_response(status=200, 
                             body=disc_obj.to_json(),
                             msg=f"Disco {id} Atualizado com Sucesso!")
    except:
        return send_response(status=400,
                             body={},
                             msg=f"Nao foi possivel atualizar disco {id}!")

# Remove um disco do banco de dados
@app.route("/disco/<id>", methods=["DELETE"])
def delete(id):
    disc_obj = Discos.query.filter_by(id=id).first()

    try:
        db.session.delete(disc_obj)
        db.session.commit()
        return send_response(status=200,
                             body=disc_obj.to_json(),
                             msg=f"Disco {id} deletado com sucesso!")
    except:
        return send_response(status=400,
                             body={},
                             msg=f"Nao foi possivel deletar o disco {id}!")


def send_response(status: int, body, msg):
    corpo = {}
    corpo["disco"] = body
    corpo["mensagem"] = msg
    return Response(json.dumps(corpo), status=status, mimetype="application/json")

app.run()