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
    MAIL_SERVER=os.getenv('MAIL_SERVER', 'sv14578.xserver.jp')
    MAIL_PORT=os.getenv('MAIL_PORT', "465")
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', "False").lower() == "true"
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', "True").lower() == "true"
    MAIL_USERNAME= os.getenv('MAIL_USERNAME', "noreply@cosydashboard.com")
    MAIL_PASSWORD= os.getenv('MAIL_PASSWORD', "tamon100")
    MAIL_DEFAULT_SENDER= os.getenv('MAIL_DEFAULT_SENDER', "noreply@cosydashboard.com")
    ADMINISTRATOR_EMAIL= os.getenv('MAIL_DEFAULT_ADMINISTRATOR', "smpcosy@gmail.com")
    ACCESS_USERNAME = os.getenv('ACCESS_USERNAME', 'admin')
    ACCESS_PASSWORD = os.getenv('ACCESS_PASSWORD', 'admin123')
    PRODUCTION = os.getenv('PRODUCTION', 0)
    PUBLIC_URL = os.getenv('PUBLIC_URL', "https://acquire-cape-cylinder-partnerships.trycloudflare.com/")
    DATABASE = os.getenv('DATABASE', 'postgresql') #mysql
    DB_USERNAME = os.getenv('DB_USERNAME', 'kobe9f') #root
    DB_PASS = os.getenv('DB_PASS', 'tamon100') #tamon100
    DB_SERVER = os.getenv('DB_SERVER', '192.168.12.35') #localhost
    DB_PORT = os.getenv('DB_PORT', '5432') #5432
    DB_NAME = os.getenv('DB_NAME', 'ppc_point_payment')


    
    # Language localization
    LANGUAGES = {
    'ja': '日本語',
    'en': 'English'
    } 
    BABEL_DEFAULT_LOCALE= 'ja'
    SECRET_KEY = 'your_secret_key'

    # MAIL_SERVER = 'cosy-kobe.sakura.ne.jp'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = 'cosy-container@cosy-kobe.sakura.ne.jp'  # enter your email here
    # MAIL_DEFAULT_SENDER = 'cosy-container@cosy-kobe.sakura.ne.jp'  # enter your email here
    # MAIL_PASSWORD = 'cosycube0806'  # enter your password here



