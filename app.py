from app import app

if __name__ == '__main__':
    # scheduler.add_listener(autoRemoveExpiredTransactions, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    app.run(host='0.0.0.0', port='50505', debug=True)
    # flask_app.run(host='192.168.11.45', debug=True)
