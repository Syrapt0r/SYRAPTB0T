import configparser
import json
from os import path

from syraptbot import status


def loadStats():
    status.print_status("Loading stats...")
    with open("stats.txt", "r") as conf:
        confData = conf.readlines()
        conf.close()

    statsDecode = json.loads(confData[0])
    return statsDecode


def saveStats(stats):
    status.print_status("Saving stats...")

    statsJson = json.dumps(stats)
    with open("stats.txt", "w") as conf:
        conf.write(statsJson)
        conf.close()


def readToken():
    if path.exists("token.txt"):
        configParser = configparser.RawConfigParser()
        configFile = r'token.txt'
        configParser.read(configFile)
    else:
        return None

    return configParser.get('token', 'token')
