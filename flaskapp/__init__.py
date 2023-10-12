"""Flask app for starting server."""
import os

from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask
from flask_httpauth import HTTPBasicAuth
#from flask_sqlalchemy import SQLAlchemy

load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")
port = os.getenv("DB_PORT")



print("********" * 20, user, password, host, database, port)

auth = HTTPBasicAuth()
app = Flask(__name__)
app.config["SWAGGER"] = {
    "uiversion": 3,
    "swagger": "2.0",
    "info": {
        "title": "Audit+",
        "description": "Audit+ API",
        "contact": {
            "responsibleOrganization": "Audit+",
            "responsibleDeveloper": "Joao Almeida",
        },
        "termsOfService": "http://me.com/terms",
        "version": "0.0.1",
    },
   # "host": "http://bibliovigilancia.gim.med.up.pt/",  # overrides localhost:5000
    "basePath": "api",  # base bash for blueprint registration
    "schemes": ["http", "https"],
}
swagger = Swagger(app, template=app.config["SWAGGER"])

SQLALCHEMY_DATABASE_URI = f"postgresql://{user}:{password}@{host}:{port}/{database}"

# Enter here your database informations
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI  # makes not sense. check it later

import flaskapp.views
