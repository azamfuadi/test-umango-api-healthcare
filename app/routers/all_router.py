from app import app
from app.controllers import all_controller
from app.controllers.all_controller import token_required
from flask import request, Blueprint, session, redirect, url_for, render_template, send_from_directory
import os

allroute_blueprint = Blueprint("all_router", __name__)

@app.route('/')
def landingPage():
    return render_template("index.html")

@app.route('/preview/<filename>')
def preview_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, mimetype='application/pdf')

@app.route('/admin/setting', methods=['GET'])
@token_required
def adminSetting():
    return all_controller.getAdminSetting()


@app.route('/admin/setting/logo', methods=['GET'])
@token_required
def companyLogo():
    return all_controller.getCompanyLogo()


@app.route('/user/list', methods=['GET'])
@token_required
def userList():
    return all_controller.getUserList()


@app.route('/admin/setting/update', methods=['PUT'])
@token_required
def adminUpdate():
    req = request.form
    if 'company_logo' not in request.files:
        file = ''
    else:
        file = request.files['company_logo']
    return all_controller.updateAdminSetting(file, **req)
    

@app.route('/language/<lang>')
def set_language(lang):
    session['language'] = lang
    return redirect(request.referrer or url_for('index'))
    