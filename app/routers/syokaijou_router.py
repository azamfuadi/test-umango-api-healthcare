from flask import request, render_template, jsonify
from app import app, key
from app.controllers import  syokaijou_controller
from app.controllers.all_controller import token_required
from flask import request, Blueprint
from urllib.error import *
import json
from flask_jwt_extended import jwt_required, get_jwt_identity

syokaijou_blueprint = Blueprint("syokaijou_router", __name__)


@app.route("/introduction-letters-page")
def introductionLetterPage():
    message_request = request.args.get('message')
    message = ''
    if message_request is not None:
        message = message_request
    response = syokaijou_controller.getSyokaijouList()
    syokaijou_list = json.loads(response.data)
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
        
        return syokaijou_controller.addNewSyokaijou(username, date, disease_name, introduction_purpose, summary, file_location)
    
@app.route("/api/get-all/introduction-letter")
def getAllIntroductionLetter():
    message_request = request.args.get('message')
    return syokaijou_controller.getSyokaijouList()