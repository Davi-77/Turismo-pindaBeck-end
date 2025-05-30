from flask import Flask, jsonify
from flask_cors import CORS
from routes.adicona_locais import AdicionaLocais
from routes.locais import Locais
from routes.auth import auth_user
from routes.comentarios_users import BuscaComentarios

app = Flask(__name__)

CORS(app)
AdicionaLocais(app)
Locais(app)
auth_user(app)
BuscaComentarios(app)




if '__main__' == __name__:
    app.run(debug=True)

