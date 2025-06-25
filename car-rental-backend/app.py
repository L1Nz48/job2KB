from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from mongoengine import connect
from config import Config

from routes.auth import auth
from routes.rental import rental

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
JWTManager(app)
connect(**app.config['MONGODB_SETTINGS'])

app.register_blueprint(auth, url_prefix='/api')
app.register_blueprint(rental, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
