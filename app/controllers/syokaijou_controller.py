from app import key, app, mail, db_session
from flask_babel import gettext
import datetime
import uuid
from sqlalchemy import desc
import flask_excel as excel

from app.models.syokaijou_model import tokyo, syokaijou
from app.controllers.all_controller import session_scope

#Obtaining the Syoukaijou details
def checkSyokaijouById(syokaijouId):
    selected_syokaijou = db_session.query(syokaijou).filter(syokaijou.transaction_id == syokaijouId).one()
    data = {
        'id': selected_syokaijou.id,
        'created_at': selected_syokaijou.created_at,
        'updated_at': selected_syokaijou.updated_at,
        'username': selected_syokaijou.username,
        'date': selected_syokaijou.date,
        'disease_name': selected_syokaijou.disease_name,
        'introduction_purpose': selected_syokaijou.introduction_purpose,
        'summary': selected_syokaijou.summary,
        'file_location': selected_syokaijou.file_location,
    }
    
    response = {
                'message': gettext('Success loading the letter of introduction.'),
                'code': '01',
                'data': data
    }
    return response

# Downloading the transaction log as CSV file
def downloadCSVSyokaijou():
    syokaijou_list = db_session.query(syokaijou).order_by(desc(syokaijou.updated_at))
    column_names = [ 'created_at', 'updated_at', 'username', 'date', 'disease_name', 'introduction_purpose', 'summary', 'file_location' ]
    return excel.make_response_from_query_sets(
        syokaijou_list,
        column_names,
        "xls",
        file_name=gettext('Letter of Introduction List')
    )


def getSyokaijouList():
    with session_scope() as session:
        syokaijou_list = session.query(syokaijou).order_by(desc(syokaijou.updated_at))
    result = []
    for items in syokaijou_list:
        result.append({
                    'id': items.id,
                    'created_at': items.created_at,
                    'updated_at': items.updated_at,
                    'username': items.username,
                    'date': items.date,
                    'disease_name': items.disease_name,
                    'introduction_purpose': items.introduction_purpose,
                    'summary': items.summary,
                    'file_location': items.file_location,
        }) 
    response = {
                'message': gettext('Success loading the letter of introduction list.'),
                'code': '01',
                'data': result
    }
    return response

def addNewSyokaijou(username, date, disease_name, introduction_purpose, summary, file_location):
    timestamp = tokyo.localize(datetime.datetime.now())
    string_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    specific_string_timestamp = str(timestamp.timestamp()).replace('.','_')
    syoukaijou_id = uuid.uuid4().hex[:5]+'_'+specific_string_timestamp
    with session_scope() as session:
            new_syokaijou = syokaijou(
                id = syoukaijou_id,
                created_at = timestamp,
                updated_at = timestamp,
                username = username,
                date = date,
                disease_name = disease_name,
                introduction_purpose = introduction_purpose,
                summary = summary,
                file_location = file_location
            )
            session.add(new_syokaijou)
    response = {
                'message': gettext('Success adding a new letter of introduction list.'),
                'code': '01',
                'data': {
                    'id': syoukaijou_id,
                    'created_at': string_timestamp,
                    'updated_at': string_timestamp,
                    'username': username,
                    'date': date,
                    'disease_name': disease_name,
                    'introduction_purpose': introduction_purpose,
                    'summary': summary,
                    'file_location': file_location,
        }
    }
    return response
        