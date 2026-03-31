from app import key, app, mail, db_session
import jwt
from flask_jwt_extended import *
from flask import render_template, redirect, jsonify, request, send_file, url_for
from urllib.request import urlopen
from urllib.error import *
from io import StringIO, BytesIO
from zipfile import ZipFile
import datetime
from functools import wraps
import os
from contextlib import contextmanager
from threading import Thread
from flask_mail import Message
from flask_babel import gettext

ru = u'\u30EB'

patientList= [
        {
            'id': 'patient1231',
            'name': '山田 健太',
            'birthday': '昭59年3月15日',
            'gender': '男'
        },
        {
            'id': 'patient1232',
            'name': '高橋 正人',
            'birthday': '昭50年12月2日',
            'gender': '男'
        },
        {
            'id': 'patient1233',
            'name': '佐藤 真理子',
            'birthday': '平2年7月8日',
            'gender': '女'
        },
        {
            'id': 'patient1234',
            'name': '中村 美咲',
            'birthday': '平12年5月21日',
            'gender': '女'
        },
        {
            'id': 'patient1235',
            'name': '山本健太',
            'birthday': '平6年5月18日',
            'gender': '男'
        }
    ]

@contextmanager
def session_scope():
    session = db_session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


# ==================function to send email asynchronusly

def async_send_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(subject, recipient, template, **kwargs):
    msg = Message(
        subject, sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[recipient])
    msg.html = render_template(template, **kwargs)
    thr = Thread(target=async_send_mail, args=[app, msg])
    thr.start()
    return thr

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'pdf', 'tfif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    
def jwt_or_redirect(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        token = request.cookies.get('t')
        try:
            data = jwt.decode(token, key, algorithms=['HS256'])
            if token:  # If a JWT identity is found (meaning a token exists)
                return redirect(url_for('settingPage'))
        except Exception:
            # Handle potential errors during JWT verification if needed
            pass
        return fn(*args, **kwargs)
    return decorator


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('t')
        if not token:
            # return jsonify({'message': 'Token is missing'}), 403
            body = render_template('alert/error.html', mssg=gettext("Authentication token is missing. Please login again."))
            return (body, 403)
        try:
            data = jwt.decode(token, key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            # return jsonify({'message': 'Token expired, log in again'}), 403
            body = render_template('alert/error.html', mssg=gettext("Token is expired, please reauthenticate."))
            return (body, 403)
        except jwt.InvalidTokenError:
            # return jsonify({'message': 'Invalid token. Please log in again.'}), 403
            body = render_template('alert/error.html', mssg=gettext("Token is invalid, please reauthenticate."))
            return (body, 403)

        return f(*args, **kwargs)
    return decorated

def downloadApplicationLogs():
    access_logs = os.path.join(app.config['TEMPLATE_FOLDER'], 'logs','access.log')
    error_logs = os.path.join(app.config['TEMPLATE_FOLDER'], 'logs','error.log')

    memory_file = BytesIO()

    #Insert the logs file to the zip file
    with ZipFile(memory_file, 'w') as zf:
        zf.write(access_logs, 'access.log')
        zf.write(error_logs, 'error.log')

    #Return to the beginning of the memory file
    memory_file.seek(0)

    return send_file(memory_file, mimetype='application/zip', as_attachment=True, download_name='application_logs.zip')
    


def getPatientList(): 
    result = {
        'message': gettext('Success loading patient list'),
        'code': '01',
        'data': patientList
    }
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

def findPatientByParams(id, name, birthday, gender):
    # search_result = [
    #     patient for patient in patientList
    #     if all(patient.get(k) == v for k, v in params.items())
    # ]
    search_result = [patient for patient in patientList 
                     if id in patient['id'] and name in patient['name'] and birthday in patient['birthday'] and gender in patient['gender']
                     ]
    print(search_result)
    message = ''
    if len(search_result) == 0:
        message += gettext('Patient not found')
    else :
        message += gettext('Patient found')
    result = {
        'message' : message,
        'code': '01',
        'data': search_result
    }
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
    
