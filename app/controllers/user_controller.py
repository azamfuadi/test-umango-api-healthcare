from flask import jsonify, render_template
from sqlalchemy import asc
from app.models.user_model import Admins
from flask_jwt_extended import *
from passlib.hash import sha256_crypt
import datetime
import uuid
import string    
import random
from app import db_session, app, mail
from threading import Thread
from flask_mail import Message
from app.controllers.all_controller import session_scope


@jwt_required()
def showAllAdmins():
    users = db_session.query(Admins).order_by(asc(Admins.username))
    result = []
    for items in users:
        user = {
            "userid": items.userid,
            "fullname": items.fullname,
            "username": items.username,
            "password": items.password,
            "email": items.email,
            "role": items.role,
        }
        result.append(user)
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def showUserById(**param):
    with session_scope() as session:
        dbresult = session.query(Admins).filter(
            Admins.userid == param['userid']).one()
    user = {
        "userid": dbresult.userid,
        "username": dbresult.username,
        "password": dbresult.password,
        "is_admin": dbresult.is_admin,
        "email": dbresult.email,
    }
    response = jsonify(user)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def generateToken(**param):
    dbresult_mail = db_session.query(Admins).filter(
        Admins.email == param['name_email']).first()
    dbresult_name = db_session.query(Admins).filter(
        Admins.username == param['name_email']).first()
    if dbresult_mail is not None or dbresult_name is not None:
        if dbresult_mail is not None :
            dbresult = dbresult_mail
        else :
            dbresult = dbresult_name
            
        authenticated = sha256_crypt.verify(
            param['password'], dbresult.password)
        if authenticated:
            user = {
                "userid": dbresult.userid,
                "username": dbresult.username,
                "email": dbresult.email,
                "role": dbresult.role,
                "fullname": dbresult.fullname
            }
            expires = datetime.timedelta(hours=2)
            expires_refresh = datetime.timedelta(days=3)
            access_token = create_access_token(
                user, fresh=True, expires_delta=expires)

            data = {
                "data": user,
                "token_access": access_token
            }
        else:
            data = {
                "message": "Wrong Password"
            }
    else:
        data = {
            "message": "Username or Email Not Found"
        }
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def insertUser(**params):
    with session_scope() as session:
        users = session.query(Admins).all()
    usernameList = []
    emailList = []
    for items in users:
        usernameList.append(items.username)
        emailList.append(items.email)
    
    if params['username'] in usernameList :
        data = {
            "message": "Username already exist in the database"
        }
    elif params['email'] in emailList :
        data = {
            "message": "Email already exist in the database"
        }
    else :
        uid = uuid.uuid4().hex
        with session_scope() as session:
            newUser = Admins(
                userid=uid,
                fullname=params['fullname'],
                username=params['username'],
                password=sha256_crypt.encrypt(params['password']),
                email=params['email'],
                role="Admin",
                confirmed=False
            )
            session.add(newUser)
        data = {
            "message": "Insert user success"
        }
    
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@jwt_required()
def insertUserByInvitation(**params):
    with session_scope() as session:
        users = session.query(Admins).all()
    usernameList = []
    emailList = []
    for items in users:
        usernameList.append(items.username)
        emailList.append(items.email)
    
    if params['username'] in usernameList :
        data = {
            "message": "Username already exist in the database"
        }
    elif params['email'] in emailList :
        data = {
            "message": "Email already exist in the database"
        }
    else :
        uid = uuid.uuid4().hex
        with session_scope() as session:
            newUser = Admins(
                userid=uid,
                fullname=params['fullname'],
                username=params['username'],
                password=sha256_crypt.encrypt(params['password']),
                email=params['email'],
                role="Admin",
                confirmed=False
            )
            session.add(newUser)
        
        data = {
            "message": "Insert user success"
        }
    
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@jwt_required()
def updateUser(**params):
    current = get_jwt_identity()
    with session_scope() as session:
        user = session.query(Admins).filter(Admins.userid == current['userid']).first()
    
    if params['username'] != '' :
        username = params['username']
    else :
        username = user.username

    if params['fullname'] != '' :
        fullname = params['fullname']
    else :
        fullname = user.fullname

    if params['email'] != '':
        email = params['email']
    else :
        email = user.email

    if params['newPassword'] != '':
        authenticated = sha256_crypt.verify(
            params['oldPassword'], user.password)
        if(authenticated):
            with session_scope() as session:
                session.query(Admins).filter(
                Admins.userid == current['userid']).update({
                    "username": username,
                    "fullname": fullname,
                    "password": sha256_crypt.encrypt(params['newPassword']),
                    "email": email,
                })
            message = 'Update User Success'
        else :
            message = 'Old Password not match with database'
    else :
        with session_scope() as session:
            session.query(Admins).filter(
            Admins.userid == current['userid']).update({
                "username": username,
                "fullname": fullname,
                "email": email,
            })
        message = 'Update User Success'
    response = jsonify({"message": message})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@jwt_required()
def deleteUser(**params):
    current = get_jwt_identity()
    if current['is_admin'] == 1:
        with session_scope() as session:
            session.query(Admins).filter(
                Admins.userid == params['userid']).delete()
        response = jsonify({"message": "Delete Succes"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        response = jsonify({"message": "Admin Access Only"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

#==================function to send email asynchronusly
def async_send_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(subject, recipient, template, **kwargs):
    msg = Message(subject, sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[recipient])
    msg.html = render_template(template, **kwargs)
    thr = Thread(target=async_send_mail, args=[app, msg])
    thr.start()
    return thr

def generateNewPass(**params):
    with session_scope() as session:
        dbresult = session.query(Admins).filter(
            Admins.email == params['email']).first()

    if dbresult is not None:
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 8))
        with session_scope() as session:
            session.query(Admins).filter(
                Admins.email == params['email']).update({
                    "password": sha256_crypt.encrypt(str(ran)),
            })    
        send_mail("Password Reset !", params['email'], 'mail/reset_password.html', email=params['email'],  password=str(ran))
        data = {
            "message": "An Email Has Been Sent to Your Account Regarding Your Password"
        }
    else:
        data = {
            "message": "Email Not Found"
        }
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@jwt_required()
def emailInvitation(**params):
    with session_scope() as session:
        users = session.query(Admins).all()
    emailList = []
    for items in users:
        emailList.append(items.email)

    if params['email'] in emailList :
        data = {
            "message": "Email already exist in the database"
        }
    else :
        expires = datetime.timedelta(hours=2)
        expires_refresh = datetime.timedelta(days=3)
        user = {'email' :params['email']}
        access_token = create_access_token( user, fresh=True, expires_delta=expires)

        send_mail("Testing Email Registration !", params['email'], 'mail/register_invitation.html', email=params['email'],  jwt=access_token)

        data = {
            "message": "Invitation Email Will Be Sent To Your Customer"
        }
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
