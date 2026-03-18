from flask import request, render_template, jsonify
from app import app, key
from app.controllers import  syokaijou_controller
from app.controllers.all_controller import token_required
from flask import request, Blueprint
from urllib.error import *
import jwt
from flask_jwt_extended import jwt_required, get_jwt_identity

syokaijou_blueprint = Blueprint("syokaijou_router", __name__)


@app.route("/introduction-letters-page")
def introductionLetterPage():
    message_request = request.args.get('message')
    message = ''
    if message_request is not None:
        message = message_request
    syokaijou_list = syokaijou_controller.getSyokaijouList()
    print(syokaijou_list["data"])
    return render_template("table/syokaijou.html",syokaijouList = syokaijou_list, message=message)

@app.route("/api/add/introduction-letter", methods=['POST'])
@jwt_required()
def addIntroductionLetter():
    current = get_jwt_identity()

    if len(request.form) > 0:    
        username =  request.form["username"]
        date = request.form["date"]
        disease_name =  request.form["disease_name"]
        introduction_purpose = request.form["introduction_purpose"]
        summary = request.form["summary"]
        file_location = request.form["file_location"]
    
        result = syokaijou_controller.addNewSyokaijou(username, date, disease_name, introduction_purpose, summary, file_location)
        response = jsonify(result)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return jsonify(response)
    
@app.route("/api/get-all/introduction-letter")
def getAllIntroductionLetter():
    message_request = request.args.get('message')
    message = ''
    if message_request is not None:
        message = message_request
    result = syokaijou_controller.getSyokaijouList()
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return jsonify(response)