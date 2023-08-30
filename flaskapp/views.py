import os

from flask import jsonify, request, session,render_template
from sqlalchemy import create_engine
from flaskapp import app, auth
from flaskapp.core.cache import insert_into_cache,check_action


gitcommit = os.getenv("GITHUB_SHA")

# Test if it works
print(gitcommit)

print(app.config)


engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"],execution_options={"isolation_level": "AUTOCOMMIT"})
conn = engine.connect()



@app.route("/", methods=["GET"])
def hello():
    return render_template("index.html")

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
    if "ERROR" in result:
        return jsonify({"error": result,}), 400

    return jsonify(result)

@app.route("/api/v1/evaluate_action", methods=["POST"])
@auth.login_required
# @swag_from("docs/search.yml", validation=True)  # validates data automatically
def evaluate_action():
    
    nummecsonho=request.json.get("_source").get("nummecsonho")
    ADLOCPC_2=request.json.get("_source").get("ADLOCPC:2")
    ADLOCPC_4=request.json.get("_source").get("ADLOCPC:4")
    desunidade=request.json.get("_source").get("desunidade")
    dataaccao=request.json.get("_source").get("dataaccao")

    print(nummecsonho,ADLOCPC_2,ADLOCPC_4,desunidade,dataaccao)
    result=check_action(conn,nummecsonho,ADLOCPC_2,ADLOCPC_4,desunidade,dataaccao)
   # result = makesearch(conn, terms, max_nr)
    print(result)
    return jsonify(result)
