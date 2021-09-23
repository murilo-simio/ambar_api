import json
from logging import exception

from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy

# Coloque aqui o caminho para a pasta ambar_api
PATH_TO_DATABASE = 'home/murilo/dev/'

# Configura o db
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+ PATH_TO_DATABASE + 'ambar_api/src/discos.db'
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
    elems = Discos.query.count()
    discs_json = [disc.to_json() for disc in discs_obj]
    return send_response(status=200,
                         body=discs_json,
                         msg=f"Todos os {elems} discos foram retornados com sucesso")

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

# Retorna os discos de acordo com os atributos
@app.route("/<attribute>/<value>", methods=["GET"])
def get_by_attribute(attribute: str, value):
    try:
        if attribute == "artista":
            artista_obj = Discos.query.filter_by(artista=value)
            if Discos.query.filter_by(artista=value).count() < 1:
                raise exception
        if attribute == "titulo":
            artista_obj = Discos.query.filter_by(titulo=value)
            if Discos.query.filter_by(titulo=value).count() < 1:
                raise exception
        if attribute == "genero":
            artista_obj = Discos.query.filter_by(genero=value)
            if Discos.query.filter_by(genero=value).count() < 1:
                raise exception
        if attribute == "valor":
            artista_obj = Discos.query.filter_by(valor=value)
            if Discos.query.filter_by(valor=value).count() < 1:
                raise exception
        disc_artista = [disc.to_json() for disc in artista_obj]
        return send_response(status=200,
                             body=disc_artista,
                             msg=f"Os discos com {attribute}: {value} foram "
                                  "retornados com sucesso!")
    except:
        return send_response(status=400,
                             body={},
                             msg=f"Erro ao buscar discos de {attribute} = {value}!")

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
        if "titulo" in body:
            setattr(disc_obj, "titulo", body["titulo"])
        elif "genero" in body:
            setattr(disc_obj, "genero", body["genero"])
        elif "artista" in body:
            setattr(disc_obj, "artista", body["artista"])
        elif "valor" in body:
            setattr(disc_obj, "valor", body["valor"])
        else:
            raise exception
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