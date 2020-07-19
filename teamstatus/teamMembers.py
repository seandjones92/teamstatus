#!/usr/bin/env python

import os
from datetime import datetime

import sqlite3
from slack import WebClient
from slack.errors import SlackApiError


class teamMember(object):
    """class for working with users"""

    def __init__(self, slackId, channelId):
        """takes the slack user ID and gets the users information from the DB"""
        # save slackId internally
        self.slackId = (slackId,)

        # save channel id we are interacting with
        self.channelId = (channelId,)

        # set DB location
        self.dblocation = '/data/teamstatus.db'

        # connect to DB and create cursor
        conn = sqlite3.connect(self.dblocation)
        cur = conn.cursor()

        # get users current information
        self.userName = cur.execute(
            "SELECT NAME FROM users WHERE SLACKID = ?;", self.slackId)
        self.lastUpdated = cur.execute(
            "SELECT LASTUPDATED FROM users WHERE SLACKID = ?;", self.slackId)
        self.userStatus = cur.execute(
            "SELECT STATUS FROM users WHERE SLACKID = ?;", self.slackId)  # SELECT SHORTSTAT from status WHERE ID = (SELECT STATUS FROM users WHERE NAME = 'username');

        # close db connection
        conn.close()

    def __updateDB(self):
        """update the users status in the DB"""
        conn = sqlite3.connect(self.dblocation)
        cur = conn.cursor()

        # set user status in DB
        cur.execute("UPDATE users SET LASTUPDATED = ?, STATUS = ? WHERE SLACKID = ?",
                    (self.lastUpdated, self.userStatus, self.slackId))

        conn.commit()
        conn.close()

        return True

    def __updateSlack(self):
        """update the users status in the slack client"""
        client = WebClient(token=os.environ['SLACK_API_TOKEN'])

        try:
            response = client.chat_postEphemeral(
                channel=self.channelId,
                user=self.slackId,
                text="Status changed")
            assert response["message"]["text"] == "Status changed"
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            print(f"Got an error: {e.response['error']}")

        return True

    def __usableStatus(self, userText):
        """Take what the user entered and convert it to the standard status"""
        statusLunch = {"lunch": ["food", "monch", "nom"]}
        statusBreak = {"break": ["walk", "brb"]}
        statusBack = {"back": ["back"]}
        statusOnline = {"online": ["hello", "good morning"]}
        statusEod = {"eod": ["eod", "good night"]}
        statusList = [statusLunch, statusBreak,
                      statusBack, statusOnline, statusEod]

        for dict in statusList:
            for key in dict:
                for value in key:
                    if userText == value:
                        userStatus = str(key)

        return userStatus

    def updateStatus(self, userText):
        """Update the user status and set last updated time"""
        # update the variables
        self.lastUpdated = datetime.now()
        self.userStatus = self.__usableStatus(userText)
        # update the values held in the db and the slack client
        self.__updateDB()
        self.__updateSlack()
