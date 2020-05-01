import os
from datetime import datetime

import psycopg2
from flask import Flask, abort, jsonify, request

app = Flask(__name__)


def is_request_valid(request):
    is_token_valid = request.form['token'] == os.environ['SLACK_VERIFICATION_TOKEN']
    is_team_id_valid = request.form['team_id'] == os.environ['SLACK_TEAM_ID']

    return is_token_valid and is_team_id_valid


def setUserText(activeUser, userText, currentTime):
    """Set the users status"""
    userStatus = usableStatus('userText')

    updateDB(activeUser, userStatus, currentTime)
    updateSlack(activeUser, userStatus)
    return True


def userReport():
    """Return the status of all users in the channel"""
    return True


def usableStatus(userText):
    """Take what the user entered and convert it to the standard status"""
    statusLunch = {"lunch": ["food", "monch", "nom"]}
    statusBreak = {"break": ["walk", "brb"]}
    statusBack = {"back": ["back"]}
    statusOnline = {"online": ["hello", "good morning"]}
    statusEod = {"eod": ["eod", "good night"]}
    statusList = [statusLunch, statusBreak,
                  statusBack, statusOnline, statusEod]

    newText = str(userText).lower()

    for dict in statusList:
        for key in dict:
            for value in key:
                if newText == value:
                    userStatus = str(key)

    return userStatus


@app.route('/teamstatus', methods=['POST'])
def teamstatus():
    if not is_request_valid(request):
        abort(400)

    activeUser = request.form['user_id']
    userText = request.form['text']

    now = datetime.now()
    currentTime = now.strftime("%H:%M")

    if userText == "report":
        response = userReport()
    else:
        setUserText(activeUser, userText, currentTime)

    return response
