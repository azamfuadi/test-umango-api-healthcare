from app import key, app, mail, db_session
from flask_babel import gettext
import datetime
import uuid
from sqlalchemy import desc
import flask_excel as excel
from flask import jsonify
from werkzeug.utils import secure_filename
from app.models.monshinhyou_model import tokyo, monshinhyou
from app.controllers.all_controller import session_scope, allowed_file
import os

#Obtaining the Syoukaijou details
def checkMonshinhyouById(monshinhyouId):
    selected_monshinhyou = db_session.query(monshinhyou).filter(monshinhyou.transaction_id == monshinhyouId).one()
    data = {
        'id': selected_monshinhyou.id,
        'created_at': selected_monshinhyou.created_at,
        'updated_at': selected_monshinhyou.updated_at,
        'username': selected_monshinhyou.username,
        'date': selected_monshinhyou.date,
        'patient_name': selected_monshinhyou.patient_name,
        'gender': selected_monshinhyou.gender,
        'birthday': selected_monshinhyou.birthday,
        'symptoms': selected_monshinhyou.symptoms,
        'current_illness': selected_monshinhyou.current_illness,
        'medication': selected_monshinhyou.medication,
        'food_allergies': selected_monshinhyou.food_allergies,
        'drug_allergies': selected_monshinhyou.drug_allergies,
        'medical_history': selected_monshinhyou.medical_history,
        'drinking_habits': selected_monshinhyou.drinking_habits,
        'smoking_habits': selected_monshinhyou.smoking_habits,
        'file_location': selected_monshinhyou.file_location,
        'file_url': selected_monshinhyou.file_url,
    }
    
    result = {
                'message': gettext('Success loading the medical questionnaire.'),
                'code': '01',
                'data': data
    }
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Downloading the transaction log as CSV file
def downloadCSVMonshinhyou():
    monshinhyou_list = db_session.query(monshinhyou).order_by(desc(monshinhyou.updated_at))
    column_names = [ 'created_at', 'updated_at', 'username', 'date', 'patient_name', 'gender', 'birthday', 'symptoms', 'current_illness', 'medication', 'food_allergies', 'drug_allergies', 'medical_history', 'drinking_habits', 'smoking_habits', 'file_location', 'file_url' ]
    return excel.make_response_from_query_sets(
        monshinhyou_list,
        column_names,
        "xls",
        file_name=gettext('Medical Questionnaire List')
    )


def getMonshinhyouList():
    with session_scope() as session:
        monshinhyou_list = session.query(monshinhyou).order_by(desc(monshinhyou.updated_at))
    result = []
    for items in monshinhyou_list:
        result.append({
                    'id': items.id,
                    'created_at': items.created_at,
                    'updated_at': items.updated_at,
                    'username': items.username,
                    'date': items.date,
                    'patient_name': items.patient_name,
                    'gender': items.gender,
                    'birthday': items.birthday,
                    'symptoms': items.symptoms,
                    'current_illness': items.current_illness,
                    'medication': items.medication,
                    'food_allergies': items.food_allergies,
                    'drug_allergies': items.drug_allergies,
                    'medical_history': items.medical_history,
                    'drinking_habits': items.drinking_habits,
                    'smoking_habits': items.smoking_habits,
                    'file_location': items.file_location,
                    'file_url': items.file_url,
        }) 
    result = {
                'message': gettext('Success loading the medical questionnaire list.'),
                'code': '01',
                'data': result
    }
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

def addNewMonshinhyou(file, username, date, patient_name, gender, birthday, symptoms, current_illness, medication, food_allergies, drug_allergies, medical_history, drinking_habits, smoking_habits, file_location):
    timestamp = tokyo.localize(datetime.datetime.now())
    string_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    specific_string_timestamp = str(timestamp.timestamp()).replace('.','_')
    monshinhyou_id = uuid.uuid4().hex[:5]+'_'+specific_string_timestamp

    file_url = ''
    print(file.filename)
    if file != '' and allowed_file(file.filename):
        print(file.filename)
        filename = file.filename
        if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
            print("The file has been deleted successfully")
            file_url = specific_string_timestamp+"_"+filename
        else:
            file_url = filename
            print("The file does not exist!")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_url))
    else: 
        print("Unsupported file")
        
    with session_scope() as session:
            new_monshinhyou = monshinhyou(
                id = monshinhyou_id,
                created_at = timestamp,
                updated_at = timestamp,
                username = username,
                date = date,
                patient_name= patient_name,
                gender= gender,
                birthday= birthday,
                symptoms= symptoms,
                current_illness= current_illness,
                medication= medication,
                food_allergies= food_allergies,
                drug_allergies= drug_allergies,
                medical_history= medical_history,
                drinking_habits= drinking_habits,
                smoking_habits= smoking_habits,
                file_location= file_location,
                file_url= file_url,
                
            )
            session.add(new_monshinhyou)
    result = {
                "message": gettext('Success adding a new letter of introduction list.'),
                "code": "01",
                "data": {
                    "id": monshinhyou_id,
                    "created_at": string_timestamp,
                    "updated_at": string_timestamp,
                    "username": username,
                    "date": date,
                    "patient_name": patient_name,
                    "gender": gender,
                    "birthday": birthday,
                    "symptoms": symptoms,
                    "current_illness": current_illness,
                    "medication": medication,
                    "food_allergies": food_allergies,
                    "drug_allergies": drug_allergies,
                    "medical_history": medical_history,
                    "drinking_habits": drinking_habits,
                    "smoking_habits": smoking_habits,
                    "file_location": file_location,
                    "file_url": file_url,
        }
    }
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
        