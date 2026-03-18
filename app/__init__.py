from app.config import Config
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask.json import JSONEncoder
from datetime import date
from werkzeug.middleware.proxy_fix import ProxyFix
import os
from flask import Flask
from flask_babel import Babel
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy_session import flask_scoped_session
from cryptography.fernet import Fernet
import flask_excel
# -*- coding: utf-8 -*-


# Creating custom JSON encoder for API response
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

# Initializing the Flask Application
app = Flask(__name__)
babel = Babel(app)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_port=1)
app.secret_key = "key"
app.config.from_object(Config)
app.json_encoder = CustomJSONEncoder
cors = CORS(app)
key = app.config['SECRET_KEY']
jwt = JWTManager(app)
mail = Mail(app)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
flask_excel.init_excel(app)

# Inserting the database credentiials
# url = 'mysql+mysqlconnector://dbmasteruser:>0&b0z02rsN-~M[Gny3YM=YBzkcUgMM7@ls-912c29a641fcdb7c731eec956e4b36c8c1a643aa.c6vcr3vpaybq.ap-northeast-1.rds.amazonaws.com/PaymentGateway'
url = 'sqlite:///app/test-data.db'

Base = declarative_base()
engine = db.create_engine(url)
db_session = flask_scoped_session(sessionmaker(bind=engine))

from app.routers.all_router import *
from app.routers.user_router import *
from app.routers.syokaijou_router import *

app.register_blueprint(allroute_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(syokaijou_blueprint)

@app.context_processor
def inject_languages():
    return {
        'languages': app.config['LANGUAGES'],
        'current_language': session.get('language') or get_locale()
    }

#Babel helper function 
def get_locale():
    if 'language' in session:
        return session['language']
    return request.accept_languages.best_match(list(app.config['LANGUAGES'].keys()))  
babel.init_app(app, locale_selector=get_locale)
