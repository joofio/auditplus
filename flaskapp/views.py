import os

from flask import jsonify, redirect, render_template, request, session
from sqlalchemy.sql import text
from sqlalchemy import create_engine
from flaskapp import app, auth


gitcommit = os.getenv("GITHUB_SHA")

# Test if it works
print(gitcommit)

print(app.config)


#def conn_creation(db):
    # try:
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
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
    terms = request.json["terms"]
    try:
        max_nr = request.json["max_nr"]
    except KeyError:
        max_nr = None
   # result = makesearch(conn, terms, max_nr)
    return jsonify(result)

