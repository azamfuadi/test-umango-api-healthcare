from app import key, app, mail, db_session
import os
import csv
from flask_babel import gettext
from werkzeug.utils import secure_filename
from io import StringIO, BytesIO
from flask import send_file
import datetime
import uuid
from sqlalchemy import desc
import flask_excel as excel

from app.models.transaction_model import transaction, tokyo
from app.controllers.all_controller import session_scope



ALLOWED_EXTENSIONS = set(['csv'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def getPaperCutPaymentConfigFile():
    filename = os.path.join(app.config['UPLOAD_FOLDER'], 'point_price.csv')
    data = []
    print(os.path.join(app.config['UPLOAD_FOLDER']))
    if not os.path.exists(filename):
        template_filename = os.path.join(app.config['TEMPLATE_FOLDER'], 'point_price.csv')
        with open(template_filename, encoding='CP932') as file:
            csv_file = csv.reader(file)
            count =0
            for row in csv_file:
                if(count>0):
                    data.append({
                        'index': count,
                        'price': row[0],
                        'points': row[1]
                    })
                count += 1
            response = {
                'message': gettext('Cannot find the price configuration file. Using the template file, please upload a new csv file containing the configuration.'),
                'data': data
            }
            return response
    else:
        with open(filename, encoding='CP932') as file:
            csv_file = csv.reader(file)
            count =0
            for row in csv_file:
                if(count>0):
                    data.append({
                        'index': count,
                        'price': row[0],
                        'points': row[1]
                    })
                count += 1
            response = {
                'message': gettext('Success loading the price configuration file.'),
                'code': '01',
                'data': data
            }
            return response

def is_integer_no_space(s):
    s_stripped = s.strip()
    try:
        int(s_stripped)
        return True
    except ValueError:
        return False

def uploadPaperCutPaymentConfigFile(file):
    if file != '' and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(app.config['UPLOAD_FOLDER'])
        if filename != 'point_price.csv':
            response = {
                'message': gettext('The file name is not as expected, please set the file name to point_price.csv'),
                'code': '02'
            }   
            return response    
        else:
            stream = StringIO(file.stream.read().decode("CP932"))
            csv_file = csv.reader(stream)
            # Get the header row
            header = next(csv_file)

            # Read the rest of the data
            # data = [row for row in csv_file]

            # You can now process 'header' and 'data'
            # For demonstration, let's just print them
            print("Header:", header)
            # print("Data:", data)
            # count =0
            for row in csv_file:
                price = row[0]
                points = row[1]
                print("Price: ", price, ", Point: ", points)
                if is_integer_no_space(price) == False or is_integer_no_space(points) == False:
                    response = {
                        'message': gettext('Please provide only integer values without any spaces.'),
                        'code': '03',
                    }
                    return response
                
            # Creating the byteIO object from the StringIO Object
            stream.seek(0)
            if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                print("The file has been deleted successfully")
            else:
                print("The file does not exist!")
            output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            with open(output_filepath, 'w', newline='', encoding='CP932') as f: # newline='' is important for CSV
                f.write(stream.read())
            response = {
                # 'totalPurchase': totalPurchase,
                'message': gettext('Success updating PaperCut Points Pricing'),
                'code': '00'
            }   
            return response
    else: 
        response = {
            # 'totalPurchase': totalPurchase,
            'message': gettext('Failed updating PaperCut Points Pricing. Please check your uploaded file type.'),
            'code': '01'
        }   
        return response

def downloadSamplePaymentConfigFile():
    filename = os.path.join(app.config['TEMPLATE_FOLDER'], 'point_price.csv')
    return send_file(filename, as_attachment=True)

def getPaperCutPaymentPrice():
    payment_price = db_session.query(price).all()
    data = []
    count = 1
    for items in payment_price:
        data.append({
                    'index': count,
                    'id': items.id,
                    'price': items.price,
                    'points': items.points
        }) 
        count+=1
    response = {
                'message': gettext('Success loading the price configuration file.'),
                'code': '01',
                'data': data
    }
    return response

#Adding new Payment Price
def addNewPaymentPrice(new_price, new_points):
    payment_price = db_session.query(price).all()
    priceList = []
    pointsList = []
    for items in payment_price:
        priceList.append(items.price)
        pointsList.append(items.points)
    
    if new_price in priceList or new_points in pointsList:
        response = {
            "message": "Price or points already in the list",
            'code': '01',
        }
    else:
        with session_scope() as session:
            newPrice = price(
                price = new_price,
                points = new_points,
            )
            session.add(newPrice)
        response = {
                'message': gettext('Success updating PaperCut Points Pricing'),
                'code': '00'
            }

    return response

#Updating current Payment Price
def updatePaymentPrice(priceId, new_price, new_points):
    with session_scope() as session:
        session.query(price).filter(
            price.id == priceId).update({
                "price": new_price,
                "points": new_points,
            })
    
    response = {
        "message": "Update User Plan Data Success",
        'code': '01'
    }

    response = {
        # 'totalPurchase': totalPurchase,
        'message': gettext('Success updating PaperCut Points Pricing'),
        'code': '00'
    }   
    return response

#Generating transaction logs in CSV file
def generateCSV(user, credit, point, order_id, status):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'Paypayポイントチャージ.csv')
    temp_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'Paypayポイントチャージ_temp.csv')
    timestamp = tokyo.localize(datetime.datetime.now())
    string_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    if not os.path.exists(filepath):
        #If the CSV file not exist, create a new CSV file
        fields=[
            ['日時','PaperCutユーザ名', '金額', 'ポイントチャージ','注文ID','チャージステータス'],
            [str(string_timestamp),str(user), str(credit), str(point),str(order_id),str(status)]
        ]
        with open(filepath, 'w', newline='', encoding='CP932') as f:
            writer = csv.writer(f)
            writer.writerows(fields)
    else:
        #If the CSV file already exist, append a new line in the CSV file
        fields=[str(string_timestamp),str(user), str(credit), str(point),str(order_id), str(status)]
        found = 0

        # Check if the order id already exist in the log
        with open(filepath, encoding='CP932') as inf, open(temp_filepath, 'w', newline='', encoding='CP932') as outf:
            reader = csv.reader(inf)
            writer = csv.writer(outf)
            for line in reader:
                if line[4] == order_id:
                    writer.writerow(fields)
                    found += 1
                    break
                else:
                    writer.writerow(line)
            writer.writerows(reader)
        os.remove(filepath)
        os.rename(temp_filepath, filepath)

        # Write a new line if the order id is not exsit in the log
        if found == 0:
            with open(filepath, 'a', newline='', encoding='CP932') as f:
                writer = csv.writer(f)
                writer.writerow(fields)

#Checking the point charge status
def checkChargeStatusByOrderId(orderId):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'Paypayポイントチャージ.csv')
    found = 0
    chargeStatus = ''
    with open(filepath, encoding='CP932') as inf:
        reader = csv.reader(inf)
        for line in reader:
            if line[4] == orderId:
                chargeStatus = chargeStatus + line[5]
                found += 1
                break
    return chargeStatus

#Checking the point charge status
def checkChargeStatusByTransactionID(transactionId):
    status = ''
    if db_session.query(transaction).filter(transaction.transaction_id == transactionId).one() is not None:
        selected_transaction = db_session.query(transaction).filter(transaction.transaction_id == transactionId).one()
        status = status + selected_transaction.transaction_status
    
    return status

#Obtaining the Transaction Details
def checkTransactionByID(transactionId):
    selected_transaction = db_session.query(transaction).filter(transaction.transaction_id == transactionId).one()
    data = {
        'id': selected_transaction.id,
        'created_at': selected_transaction.created_at,
        'updated_at': selected_transaction.updated_at,
        'expired_at': selected_transaction.expired_at,
        'transaction_id': selected_transaction.transaction_id,
        'account': selected_transaction.account,
        'payment_method': selected_transaction.payment_method,
        'amount': selected_transaction.amount,
        'point': selected_transaction.point,
        'transaction_status': selected_transaction.transaction_status,
    }
    
    return data

# Downloading the transaction log as CSV file
def downloadCSVTransactionLogs():
    transactions = db_session.query(transaction).order_by(desc(transaction.updated_at))
    column_names = [ 'created_at', 'updated_at', 'expired_at', 'transaction_id', 'account', 'payment_method', 'amount', 'point', 'transaction_status', ]
    return excel.make_response_from_query_sets(
        transactions,
        column_names,
        "xls",
        file_name='Paypayポイントチャージ'
    )
    # filename = os.path.join(app.config['UPLOAD_FOLDER'], 'Paypayポイントチャージ.csv')
    # return send_file(filename, as_attachment=True)


def getTransactionsLogs():
    with session_scope() as session:
        transactions = session.query(transaction).order_by(desc(transaction.updated_at))
    result = []
    for items in transactions:
        result.append({
                    'id': items.id,
                    'created_at': items.created_at,
                    'updated_at': items.updated_at,
                    'expired_at': items.expired_at,
                    'transaction_id': items.transaction_id,
                    'account': items.account,
                    'payment_method': items.payment_method,
                    'amount': items.amount,
                    'point': items.point,
                    'transaction_status': items.transaction_status,
        }) 
    response = {
                'message': gettext('Success loading the transaction logs.'),
                'code': '01',
                'data': result
    }
    return response

def generateTransactionLogs(type, user, amount, point, transaction_id, pay_method, status):
    timestamp = tokyo.localize(datetime.datetime.now())
    string_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    if type == 'new_transactions':
        expired_timestamp = tokyo.localize(datetime.datetime.now() + datetime.timedelta(minutes=5))
        string_expired_timestamp = expired_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        specific_string_timestamp = str(timestamp.timestamp()).replace('.','_')
        with session_scope() as session:
            new_transactions = transaction(
                id = transaction_id+'_'+specific_string_timestamp,
                created_at = string_timestamp,
                updated_at = string_timestamp,
                expired_at = string_expired_timestamp,
                transaction_id = transaction_id,
                account = user,
                payment_method = pay_method,
                amount = amount,
                point = point,
                transaction_status = status
            )
            session.add(new_transactions)
    else :
        with session_scope() as session:
            session.query(transaction).filter(transaction.transaction_id == transaction_id).update({
                "updated_at" : string_timestamp,
                "transaction_id" : transaction_id,
                "account" : user,
                "payment_method" : pay_method,
                "amount" : amount,
                "point" : point,
                "transaction_status" : status
            })

    
    
