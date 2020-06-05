import json
from os.path import isfile

import yaml

from syraptbot import status

try:
    from yaml import CLoader as Loader, CDumper as Dumper

except ImportError:
    status.print_status("[FILE] Using compatibility YAML converters")
    from yaml import Loader, Dumper

from syraptbot import status


def load_stats():
    status.print_status("[FILE] Loading stats...")

    try:
        with open("stats.txt", "r") as conf:
            conf_data = conf.readlines()
            conf.close()

    except IOError:
        return "STAT_LOAD_ERROR"

    stats_decode = json.loads(conf_data[0])
    return stats_decode


def save_stats(stats):
    status.print_status("[FILE] Saving stats...")

    stats_json = json.dumps(stats)

    with open("stats.txt", "w") as conf:
        conf.write(stats_json)
        conf.close()


def read_config_file():
    with open("config.txt", "r") as f:
        config_data = yaml.load(f, Loader=Loader)

    return config_data


def generate_default_config():
    data = {"token_discord": "", "guild_discord": "", "twitch_client_id": "", "twitch_client_secret": "",
            "twitch_username": ""}

    data_dump = yaml.dump(data, Dumper=Dumper)

    with open("config.txt", "w+") as f:
        f.writelines(data_dump)

    print("Generated new config in \"config.txt\". Script is now terminating.")


def read_file(file):
    with open(file, "r") as f:
        read_list = f.readlines()
        f.close()

    return read_list


def save_twitch_api_data(token_data):
    token_data_writeable = json.dumps(token_data)

    with open("files/twitchToken.txt", "w") as twitch_file:
        twitch_file.write(token_data_writeable)
        twitch_file.close()


def load_twitch_api_data():
    with open("files/twitchToken.txt", "r") as f:
        token_data = f.read()
        f.close()

    token_data_loadable = json.loads(token_data)

    return token_data_loadable


def has_twitch_api_data():
    return isfile("files/twitchToken.txt")
