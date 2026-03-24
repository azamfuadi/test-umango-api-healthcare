from flask import request, render_template, jsonify
from app import app, key
from app.controllers import  monshinhyou_controller
from app.controllers.all_controller import token_required
from flask import request, Blueprint
from urllib.error import *
import json
from flask_jwt_extended import jwt_required, get_jwt_identity

monshinhyou_blueprint = Blueprint("monshinhyou_router", __name__)


@app.route("/medical-questionnaire-page")
def medicalQuestionnairePage():
    message_request = request.args.get('message')
    message = ''
    if message_request is not None:
        message = message_request
    response = monshinhyou_controller.getMonshinhyouList()
    monshinhyou_list = json.loads(response.data)
    return render_template("table/monshinhyou.html",monshinhyouList = monshinhyou_list, message=message)

@app.route("/api/add/medical-questionnaire", methods=['POST'])
@jwt_required()
def addMedicalQuestionnaire():

    current = get_jwt_identity()

    if len(request.form) > 0:    
        username =  request.form["username"]
        date = request.form["date"]
        patient_name =  request.form["patient_name"]
        gender =  request.form["gender"]
        birthday =  request.form["birthday"]
        symptoms =  request.form["symptoms"]
        current_illness =  request.form["current_illness"]
        medication =  request.form["medication"]
        food_allergies =  request.form["food_allergies"]
        drug_allergies =  request.form["drug_allergies"]
        medical_history =  request.form["medical_history"]
        drinking_habits =  request.form["drinking_habits"]
        smoking_habits =  request.form["smoking_habits"]
        file_location = request.form["file_location"]
        file_encryption = request.form["file_encryption"]

        if(file_encryption):
            file = request.form["pdf_file"]
            filename = request.form["filename"]
        else:
            file = request.files['pdf_file']
            filename = request.files['filename']    
        

        # if 'pdf_file' not in request.files:
        #     file = ''
        #     filename = ''
        # else:
        #     file = request.files['pdf_file']
        #     filename = request.files['filename']
        
        return monshinhyou_controller.addNewMonshinhyou(file_encryption, file, filename, username, date, patient_name, gender, birthday, symptoms, current_illness, medication, food_allergies, drug_allergies, medical_history, drinking_habits, smoking_habits, file_location)
    
@app.route("/api/get-all/medical-questionnaire")
def getAllMedicalQuestionnaire():
    return monshinhyou_controller.getMonshinhyouList()