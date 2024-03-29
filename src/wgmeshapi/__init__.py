"""
Create Flask app instance with specific configurations. Make an API with Flask
app as context. Create database context, and import the API resources.
"""
from flask import Flask, Blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wgmeshapi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
api_bp = Blueprint('api', __name__)
api = Api(api_bp)
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

from wgmeshapi import routes
from wgmeshapi import resources
