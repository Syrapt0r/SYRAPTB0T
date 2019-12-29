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


def readTokenFile():
    configFile = 'token.txt'
    tokenData = {"token": "", "token_twitch": ""}

    if path.exists(configFile):
        configParser = configparser.RawConfigParser()
        configParser.read(configFile)
    else:
        tokenData["token"] = "NO_TOKEN_FILE"
        tokenData["token_twitch"] = "NO_TOKEN_FILE"
        return tokenData

    if configParser.has_option("token", "token"):
        tokenData["token"] = configParser.get("token", "token")
    else:
        tokenData["token"] = "MALFORMED_TOKEN_FILE"

    if configParser.has_option("token", "token_twitch"):
        tokenData["token_twitch"] = configParser.get("token", "token_twitch")
    else:
        tokenData["token_twitch"] = "MALFORMED_TOKEN_FILE"

    return tokenData


def readFile(file):
    with open(file, "r") as f:
        readList = f.readlines()
        f.close()

    return readList
