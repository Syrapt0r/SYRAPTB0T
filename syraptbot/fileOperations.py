import configparser
import json
from os import path

from syraptbot import status


def load_stats():
    status.print_status("Loading stats...")

    try:
        with open("stats.txt", "r") as conf:
            conf_data = conf.readlines()
            conf.close()

    except IOError:
        return "STAT_LOAD_ERROR"

    stats_decode = json.loads(conf_data[0])
    return stats_decode


def save_stats(stats):
    status.print_status("Saving stats...")

    stats_json = json.dumps(stats)

    with open("stats.txt", "w") as conf:
        conf.write(stats_json)
        conf.close()


def read_token_file():
    config_file = 'token.txt'
    token_data = {"token": "", "token_twitch": ""}

    if path.exists(config_file):
        config_parser = configparser.RawConfigParser()
        config_parser.read(config_file)
    else:
        token_data["token"] = "NO_TOKEN_FILE"
        token_data["token_twitch"] = "NO_TOKEN_FILE"
        return token_data

    if config_parser.has_option("token", "token"):
        token_data["token"] = config_parser.get("token", "token")
    else:
        token_data["token"] = "MALFORMED_TOKEN_FILE"

    if config_parser.has_option("token", "token_twitch"):
        token_data["token_twitch"] = config_parser.get("token", "token_twitch")
    else:
        token_data["token_twitch"] = "MALFORMED_TOKEN_FILE"

    return token_data


def read_file(file):
    with open(file, "r") as f:
        read_list = f.readlines()
        f.close()

    return read_list
