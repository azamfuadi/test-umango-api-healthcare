from flask import request, render_template, jsonify, redirect, url_for
from app import app
from app.controllers import sb_controller
from app.controllers.transaction_controller import generateTransactionLogs, getPaperCutPaymentPrice
from app.controllers.all_controller import form_token_required
from app.models.papercut_model import papercut
from flask_babel import gettext
from flask import request, Blueprint
from datetime import datetime
import uuid

sbroute_blueprint = Blueprint("sb_router", __name__)

@app.route('/update-sb-settings', methods=["POST"])
@form_token_required
def updateSbSettings():
  if len(request.form) > 0:    
    sb_merchant_id =  request.form["sb_merchant_id"]
    sb_service_id = request.form["sb_service_id"]
    sb_hash_key_link = request.form["sb_hash_key_link"]

    testParametersResult = sb_controller.testSBParameters(sb_merchant_id, sb_service_id, sb_hash_key_link)
    if testParametersResult['html_contains_error'] == 1:
        message = gettext('There are error in SB Payment parameters. Changes are not saved.')
    else :
        response = sb_controller.setSBConfig(sb_merchant_id,sb_service_id,sb_hash_key_link)
        message = response['message']
    return redirect(url_for('settingPage',  message=message))


@app.route('/responseConfirmation', methods=["POST"])
def responseConfirmation():
    order_id = request.form["order_id"]
    cust_code = request.form["cust_code"]
    amount = request.form["amount"]
    res_result = request.form["res_result"]
    res_pay_method = request.form["res_pay_method"]
    try:
        response = sb_controller.paymentCheck(order_id, cust_code, amount, res_result, res_pay_method)
        return response
    except:
        return "NG"

@app.route('/successConfirmation', methods=('GET','POST'))
def successConfirmation():
    order_id = request.form["order_id"]
    cust_code = request.form["cust_code"]
    amount = request.form["amount"]
    res_pay_method = request.form["res_pay_method"]
    return sb_controller.successURL(order_id, cust_code, amount, res_pay_method)

@app.route('/generate-hash-string', methods=('GET','POST'))
def testGeneratingHashString():
    #Parameter for sending to SB Payment
    redirect_baseUrl = request.form['redirect_url']
    merchant_id = request.form["merchant_id"]
    service_id = request.form["service_id"]
    hash_key = request.form['hash_key']
    pay_method = request.form["pay_method"]
    cust_code = request.form["cust_code"]
    amount = request.form["amount"]
    order_id = 'sb_'+uuid.uuid4().hex #Auto-generated
    item_id = request.form["item_id"]
    pay_type = '0' 
    service_type = '0' 
	# success_url = f"{puplic_url}/successConfirmation?amount={quote_plus(f.encrypt(amount.encode()))}"
    success_url = request.form["success_url"]
    cancel_url = request.form["cancel_url"]
    error_url = request.form["error_url"]
    pagecon_url = request.form["pagecon_url"]
		
    now = datetime.now() #fix the import
    request_date = (str(now.year) +sb_controller.pad2(now.month) +sb_controller.pad2(now.day) +sb_controller.pad2(now.hour) +sb_controller.pad2(now.minute) +sb_controller.pad2(now.second)) #fix the import
    limit_second = '600'
            
    string_for_link=sb_controller.compose_string(pay_method, merchant_id, service_id, cust_code, order_id, item_id, amount, pay_type, service_type, success_url, cancel_url, error_url, pagecon_url, request_date, limit_second, hash_key)
    hashed_string_link = sb_controller.get_sha1_hash_of_utf8_string(string_for_link)
    concatinated_params =({'pay_method': pay_method, 'merchant_id':merchant_id, 'service_id':service_id, 'cust_code':cust_code, 'order_id':order_id,
	    'item_id':item_id, 'amount':amount, 'pay_type':pay_type,'service_type':service_type,'success_url':success_url,'cancel_url':cancel_url,'error_url':error_url,
		'pagecon_url':pagecon_url,'request_date':request_date,'limit_second':limit_second, 'sps_hashcode':hashed_string_link})
    
    parameters = concatinated_params
    redirect_url = redirect_baseUrl+ ("?" + sb_controller.urlencode(parameters) if parameters else "")
    redirect_url_html = sb_controller.get_redirected_url_html(redirect_url)
    html_contains_error = 0
    if 'エラー' in redirect_url_html or 'sorry' in redirect_url_html:
        html_contains_error = 1

    api_response = {
        'params_list': concatinated_params,
        'concatinated_params': string_for_link,
        'hashed_string_link' : hashed_string_link,
        'redirect_url': redirect_url,
        'html_contains_error': html_contains_error,
        'redirect_url_html': redirect_url_html,
    }
    return jsonify(api_response), 200
    return redirect(redirect_url)




@app.route('/cancel', methods=('GET','POST'))
def cancel():
    # order_id = request.form["order_id"]
    # cust_code = request.form["cust_code"]
    # amount = request.form["amount"]
    # res_pay_method = request.form["res_pay_method"]
    # papercutPaymentConfig = getPaperCutPaymentPrice()
    # first_match = next((obj for obj in papercutPaymentConfig['data'] if obj['price'] == amount), None)
    # generateTransactionLogs('cancelled_charge', cust_code, amount, first_match['points'], order_id, res_pay_method, 'Payment Cancelled')
    return "Transaction cancelled"

@app.route('/error', methods=('GET','POST'))
def error():
    # order_id = request.form["order_id"]
    # cust_code = request.form["cust_code"]
    # amount = request.form["amount"]
    # res_pay_method = request.form["res_pay_method"]
    # papercutPaymentConfig = getPaperCutPaymentPrice()
    # adminEmail = app.config['ADMINISTRATOR_EMAIL']
    # first_match = next((obj for obj in papercutPaymentConfig['data'] if obj['price'] == amount), None)
    # generateTransactionLogs('failed_charge', cust_code, amount, first_match['points'], order_id, res_pay_method, 'Payment Success, Charge Failed')
    # send_mail(gettext("Papercut Points Purchase Failed Notification"), adminEmail, 'mail/admin_notification.html', transaction_id=order_id,
    #     payment_method="PayPay",  credit=first_match['points'], amount=amount, user=cust_code, logs_url='/transaction-logs' )
    # papercut_settings = session.query(papercut).filter(papercut.id == 1).one()
    # body = render_template('alert/error.html', mssg=gettext("There is a problem with the transaction, please contact the administrator"), papercut_server=papercut_settings.papercut_server)
    # return (body, 403)
    return "There is a problem with the transaction, please contact the administrator"