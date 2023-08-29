import os

from flask import jsonify, request, session
from sqlalchemy.sql import text
from sqlalchemy import create_engine
from flaskapp import app, auth
from flaskapp.core.cache import insert_into_cache,check_action

gitcommit = os.getenv("GITHUB_SHA")

# Test if it works
print(gitcommit)

print(app.config)


#def conn_creation(db):
    # try:
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"],execution_options={"isolation_level": "AUTOCOMMIT"})
#    engine = db.get_engine(app=app)
    #   print(engine)
    #  except Exception as e:
    #    print(f"Error connecting to MariaDB Platform: {e}")
    #   print()
conn = engine.connect()
 #   return conn


#conn = conn_creation(db)
@app.route("/", methods=["GET"])
def hello():

    return "hello world"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["username"] = request.form["username"]
        session["email"] = request.form["email"]
    return ""


# https://blog.miguelgrinberg.com/post/restful-authentication-with-flask
@auth.verify_password
def verify_password(username, password):
    if username != "admin" and password != "admin":
        return False
    return True




@app.route("/api/v1/filldata", methods=["POST"])
@auth.login_required
# @swag_from("docs/search.yml", validation=True)  # validates data automatically
def filldata():
    
    nummecanografico=request.json.get("_source").get("nummecanografico")
    resultado=request.json.get("_source").get("resultado")
    localpicagem=request.json.get("_source").get("localpicagem")
    datahora=request.json.get("_source").get("datahora")

    print(nummecanografico,resultado,localpicagem,datahora)
    result=insert_into_cache(conn,nummecanografico,resultado,localpicagem,datahora)
   # result = makesearch(conn, terms, max_nr)
    return jsonify(result)

@app.route("/api/v1/evaluate_action", methods=["POST"])
@auth.login_required
# @swag_from("docs/search.yml", validation=True)  # validates data automatically
def evaluate_action():
    
    nummecanografico=request.json.get("_source").get("nummecanografico")
    resultado=request.json.get("_source").get("resultado")
    localpicagem=request.json.get("_source").get("localpicagem")
    datahora=request.json.get("_source").get("datahora")

    print(nummecanografico,resultado,localpicagem,datahora)
    result=check_action(conn,nummecanografico,resultado,localpicagem,datahora)
   # result = makesearch(conn, terms, max_nr)
    return jsonify(result)
