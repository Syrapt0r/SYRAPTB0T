import json
import configparser
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
    configParser = configparser.RawConfigParser()
    configFile = r'token.txt'
    configParser.read(configFile)

    return configParser.get('token', 'token')
