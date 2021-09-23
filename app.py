import json

from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy

# Coloque aqui o caminho para a pasta ambar_api
PATH_TO_DATABASE = 'home/murilo/dev/'

# Configura o db
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+ PATH_TO_DATABASE + 'ambar_api/database.db'
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
                "genereo": self.genero,
                "artista": self.artista,
                "valor": self.valor}

# Retorna todos os discos
@app.route("/discos", methods=["GET"])
def get_all():
    discs_obj = Discos.query.all()
    discs_json = [disc.to_json() for disc in discs_obj]
    msg = 'Retrieved all discs!'
    return send_response(200, discs_json, msg)

# Retorna apenas um disco
@app.route("/disco/<id>", methods=["GET"])
def get_one(id: int):
    try:
        disc_obj = Discos.query.filter_by(id=id).first()
        disc_json = disc_obj.to_json()
        msg = "Disco retornado com sucesso"
        return send_response(200, disc_json, msg)
    except:
        msg = f"Nao foi possivel retornar o disco de id: {id}!"
        return send_response(400, {}, msg)

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
        msg = "Disco Adicionado com sucesso!"
        return send_response(201, disc.to_json(), msg)
    except:
        msg = "Nao foi possivel criar novo disco!"
        return send_response(400, body, msg)

# Atualiza um disco
@app.route("/disco/<id>", methods=["PUT"])
def update(id: int):
    disc_obj = Discos.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if "titulo" in body:
            disc_obj.titulo = body["titulo"]
        if "genero" in body:
            disc_obj.genero = body["genero"]
        if "artista" in body:
            disc_obj.artista = body["artista"]
        if "valor" in body:
            disc_obj.valor = body["valor"]

        db.session.add(disc_obj)
        db.commit()
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
                             body=disc_obj.to_json(),
                             msg=f"Nao foi possivel deletar o disco {id}!")


def send_response(status: int, body, msg):
    corpo = {}
    corpo["disco"] = body
    corpo["mensagem"] = msg
    return Response(json.dumps(corpo), status=status, mimetype="application/json")

app.run()