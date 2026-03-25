from os.path import join, dirname, realpath, abspath
import os

base_dir = abspath(dirname(__file__))

UPLOADS_PATH = join(dirname(realpath(__file__)), "static/uploads/")
TEMPLATES_PATH = join(dirname(realpath(__file__)), "templates/")

class Config(object):
    CORS_HEADERS = 'Content-Type'
    SECRET_KEY = 'ppcpaysecretkeyhehe123_dJ8-Qs7'
    FERNET_KEY= b'dJ8-Qs7ChRwBmuPJbQ0-igWdAOiN5KhLU9khvr_35Ss='
    SECURITY_PASSWORD_SALT = str(os.environ.get("SECURITY_PASSWORD_SALT"))
    JSON_SORT_KEYS = False
    JWT_SECRET_KEY = str(os.environ.get("JWT_SECRET"))
    UPLOAD_FOLDER = UPLOADS_PATH
    TEMPLATE_FOLDER = TEMPLATES_PATH


    
    # Language localization
    LANGUAGES = {
    'ja': '日本語',
    'en': 'English'
    } 
    BABEL_DEFAULT_LOCALE= 'ja'
    SECRET_KEY = 'your_secret_key'



