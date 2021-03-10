"""
Create Flask app instance with specific configurations. Make an API with Flask
app as context. Create database context, and import the API resources.
"""
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wgmeshapi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db = SQLAlchemy(app)

from wgmeshapi import resources
