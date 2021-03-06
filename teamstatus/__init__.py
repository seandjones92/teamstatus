import os
from datetime import datetime

from flask import Flask, abort, jsonify, request

from teamstatus.teamMembers import teamMember

app = Flask(__name__)


def validate_request(request):
    is_token_valid = request.form['token'] == os.environ['SLACK_VERIFICATION_TOKEN']
    is_team_id_valid = request.form['team_id'] == os.environ['SLACK_TEAM_ID']

    return is_token_valid and is_team_id_valid


@app.route('/', methods=['GET'])
def connectiontest():
    return "The web server is running"

@app.route('/teamstatus', methods=['POST'])
def teamstatus():
    if not validate_request(request):
        abort(400)

    slackId = request.form['user_id']
    userText = request.form['text'].lower()
    channelId = request.form['channel_id']

    if userText == "report":
        pass
    else:
        requestingUser = teamMember(slackId, channelId)
        requestingUser.updateStatus(userText)
