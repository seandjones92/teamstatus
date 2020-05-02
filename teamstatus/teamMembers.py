#!/usr/bin/env python

import os
from datetime import datetime

import psycopg2
from slack import WebClient
from slack.errors import SlackApiError


class teamMember(object):
    """class for working with users"""

    def __init__(self, slackId, channelId):
        """takes the slack user ID and gets the users information from the DB"""
        # save slackId internally
        self.slackId = slackId

        # save channel id we are interacting with
        self.channelId = channelId

        # connect to DB and create cursor
        conn = psycopg2.connect("dns=hostname dbname=teamdb user=teamdb")
        cur = conn.cursor()

        # get users current information
        self.userName = cur.execute(
            "SELECT NAME FROM users WHERE SLACKID = %s", self.slackId)
        self.lastUpdated = cur.execute(
            "SELECT LASTUPDATED FROM users WHERE SLACKID = %s", self.slackId)
        self.userStatus = cur.execute(
            "SELECT STATUS FROM users WHERE SLACKID = %s", self.slackId)

        # close db connection
        cur.close()
        conn.close()

    def __usableStatus(self, userText):
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

    def __updateDB(self):
        """update the users status in the DB"""
        conn = psycopg2.connect("dns=hostname dbname=teamdb user=teamdb")
        cur = conn.cursor()

        # set user status in DB
        cur.execute("UPDATE users SET LASTUPDATED = %s, STATUS = %s WHERE SLACKID = %s",
                    (self.lastUpdated, self.userStatus, self.slackId))

        cur.close()
        conn.close()

        return True

    def __updateSlack(self):
        """update the users status in the slack client"""
        client = WebClient(token=os.environ['SLACK_API_TOKEN'])

        try:
            response = client.chat_postMessage(
                channel=self.channelId,
                text="Status changed")
            assert response["message"]["text"] == "Status changed"
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            print(f"Got an error: {e.response['error']}")
        
        return True

    def updateStatus(self, userText):
        """Update the user status and set last updated time"""
        # update the variables
        self.lastUpdated = datetime.now()
        self.userStatus = self.__usableStatus(userText)
        # update the values held in the db and the slack client
        self.__updateDB()
        self.__updateSlack()
        
        return True
