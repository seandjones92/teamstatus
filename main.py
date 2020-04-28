import os

from datetime import datetime

from flask import abort, Flask, jsonify, request


app = Flask(__name__)


def is_request_valid(request):
    is_token_valid = request.form['token'] == os.environ['SLACK_VERIFICATION_TOKEN']
    is_team_id_valid = request.form['team_id'] == os.environ['SLACK_TEAM_ID']

    return is_token_valid and is_team_id_valid


@app.route('/teamstatus', methods=['POST'])
def teamstatus():
    if not is_request_valid(request):
        abort(400)

    validState = ["online", "eod", "lunch", "break"]

    activeUser = request.form['user_id']
    userText = request.form['text']
    
    now = datetime.now()
    currentTime = now.strftime("%H:%M")

    if userText in validState:
        setuserText(activeUser, userText)
        response = "your status was set"
    elif userText == "report":
        response = userReport()
    else:
        response = "invalid status"
    
    return response
