#!/usr/bin/env python

import psycopg2
from slack import WebClient
from slack.errors import SlackApiError


class userReport(object):
    """get reporting on your team members"""

    def __init__(self):
        # open connection to the DB
        conn = psycopg2.connect("dns=hostname dbname=teamdb username=teamdb")
        cur = conn.cursor()

        # init work
        cur.execute("SELECT * FROM users;")
        self.__allUserInfo = cur.fetchall()

        # close connection to the DB
        cur.close()
        conn.close()

    def sendReport(self):
        """send the report to the requestor privately"""
        # sort users by current status and bunch them together