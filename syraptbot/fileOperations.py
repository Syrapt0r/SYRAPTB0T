import configparser
import json
from os import path

from syraptbot import status


def loadStats():
    status.print_status("Loading stats...")

    try:
        with open("stats.txt", "r") as conf:
            confData = conf.readlines()
            conf.close()

    except IOError:
        return "STAT_LOAD_ERROR"

    statsDecode = json.loads(confData[0])
    return statsDecode


def saveStats(stats):
    status.print_status("Saving stats...")

    statsJson = json.dumps(stats)

    with open("stats.txt", "w") as conf:
        conf.write(statsJson)
        conf.close()


def readToken():
    configFile = 'token.txt'

    if path.exists(configFile):
        configParser = configparser.RawConfigParser()
        configParser.read(configFile)
    else:
        return "NO_TOKEN_FILE"

    if configParser.has_option('token', 'token'):
        return configParser.get('token', 'token')
    else:
        return "MALFORMED_TOKEN_FILE"


def readFile(file):

    with open(file, "r") as f:
        readList = f.readlines()
        f.close()

    return readList
