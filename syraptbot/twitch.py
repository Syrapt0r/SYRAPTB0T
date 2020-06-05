import asyncio
from datetime import datetime, timedelta
from json.decoder import JSONDecodeError
from random import randint

import requests

from syraptbot import status, fileOperations

# load live messages
live_messages = fileOperations.read_file("files/streamNotifications.txt")
status.print_status('Loaded {0} streaming notifications'.format(len(live_messages)))


class TwitchAPI:
    auth_token = ""
    auth_invalid_time = 0

    client_id = ""
    client_secret = ""

    twitch_username_list = []
    twitch_username_skip_list = {}

    guild_id = ""

    API_URL_TOKEN = "https://id.twitch.tv/oauth2/"
    API_URL_TWITCH = "https://api.twitch.tv/helix/"

    bot_reference = None

    # constructor sets all parameters needed to work with the twitch api
    def __init__(self, bot_context, token_twitch, token_secret, twitch_username, discord_guild):
        self.last_token_check = datetime.now()
        self.bot_reference = bot_context
        self.client_id = token_twitch
        self.client_secret = token_secret
        self.guild_id = discord_guild

        # if no local saved token, we request an initial one
        if fileOperations.has_twitch_api_data():
            # load local access token
            status.print_status("[TWITCH] Local access token found, loading...")
            token_data = fileOperations.load_twitch_api_data()

            self.auth_token = token_data["access_token"]
            self.auth_invalid_time = token_data["expires_in"]

            status.print_status("[TWITCH] Local access token loaded.")
        else:
            # get new access token
            status.print_status("[TWITCH] No local access token found, fetching new one...")
            self.get_access_token()

        # read user names into local array
        for name in twitch_username:
            self.twitch_username_list.append(name)

        # safety validation
        self.check_token_validity_and_request_new_if_necessary()

        status.print_status("[TWITCH] API initialized.")

    # get an initial access and refresh token
    def get_access_token(self):
        status.print_status("[TWITCH] Fetching new access token...")
        token_request = requests.post(self.API_URL_TOKEN +
                                      "token?client_id={0}&client_secret={1}&grant_type=client_credentials"
                                      .format(self.client_id, self.client_secret))

        request_data = token_request.json()

        if "access_token" in request_data:
            status.print_status("[TWITCH] Access token retrieved successfully.")
            fileOperations.save_twitch_api_data(request_data)

            self.auth_token = request_data["access_token"]

    def check_token_validity_and_request_new_if_necessary(self):
        status.print_status("[TWITCH] Validating Token {0}".format(self.auth_token))
        validation_request = requests.get(self.API_URL_TOKEN + "validate",
                                          headers={"Authorization": "OAuth {0}".format(self.auth_token)})
        data = validation_request.json()

        if "status" in data:
            if data["status"] == 401:
                status.print_status("[TWITCH] Access token invalid! Requesting new access token...")
                self.get_access_token()
        else:
            # update invalidation time
            self.auth_invalid_time = datetime.now() + timedelta(seconds=data["expires_in"] - 60)
            status.print_status("[TWITCH] Access token verified successfully!")

    def purge_and_invalidate_token(self):
        invalidation_request = requests.post(self.API_URL_TOKEN + "revoke?client_id={0}&token={1}"
                                             .format(self.client_id, self.auth_token))

        try:
            response = invalidation_request.json()

            if response["status"] == 400:
                status.print_status("[TWITCH] Error invalidating token: {0}".format(response["message"]))

        except JSONDecodeError:
            status.print_status("[TWITCH] Access token successfully invalidated.")
            return

    def auth_token_expiring_soon(self):
        return datetime.now() >= self.auth_invalid_time

    async def check_twitch_channels(self, bot):

        await bot.wait_until_ready()

        silent_mode = False

        # loop while bot runs
        while not bot.is_closed():
            # check our token is expiring soon
            if self.auth_token_expiring_soon():
                # if not, check if we need a new one before proceeding
                self.check_token_validity_and_request_new_if_necessary()

            # loop through the names and fetch stream info
            for channel in self.twitch_username_list:
                # if we are currently ignoring this user, we don't have to call the api at all
                if channel.upper() in self.twitch_username_skip_list:
                    if self.twitch_username_skip_list[channel.upper()] > datetime.now():
                        status.print_status("Ignoring {0} lol".format(channel.upper()))
                        continue

                # one time print of all checks
                if silent_mode is False:
                    status.print_status("[TWITCH] Checking user {0}...".format(channel))

                channel_info_request = requests.get(self.API_URL_TWITCH + "streams?user_login={0}".format(channel),
                                                    headers={"Client-ID": self.client_id,
                                                             "Authorization": "Bearer {0}".format(self.auth_token)})

                # convert info to json
                channel_json_info = channel_info_request.json()

                # if we have no data field, something failed. we move on.
                if not channel_json_info["data"]:
                    continue

                # otherwise, this is where the fun begins
                if channel_json_info["data"][0]["type"] == "live":
                    # extract further information
                    channel_name = channel_json_info["data"][0]["user_name"]
                    channel_link = "https://www.twitch.tv/{0}".format(channel_name)

                    # check if we post
                    if channel_name in self.twitch_username_skip_list:
                        if self.twitch_username_skip_list[channel_name] <= datetime.now():
                            status.print_status("[TWITCH] Channel {0} is live! Posting notification..."
                                                .format(channel_name))

                            for current_channel in bot.get_guild(self.guild_id).channels:
                                if current_channel.name.endswith("general"):
                                    status.print_status("[TWITCH] Found general channel, posting live message...")

                                    rand_streem_nr = randint(0, len(live_messages) - 1)
                                    await current_channel.send(live_messages[rand_streem_nr].format(channel_link))
                                    break

                            self.update_timeout_time(channel_name)
                    else:
                        status.print_status("[TWITCH] Channel {0} is live! Posting notification..."
                                            .format(channel_name))

                        for current_channel in bot.get_guild(self.guild_id).channels:
                            if current_channel.name.endswith("general"):
                                status.print_status("[TWITCH] Found general channel, posting live message...")

                                rand_streem_nr = randint(0, len(live_messages) - 1)
                                await current_channel.send(live_messages[rand_streem_nr].format(channel_link))
                                break

                        self.update_timeout_time(channel_name)

            # one time notification that pinging goes silent
            if silent_mode is False:
                status.print_status("[TWITCH] Entering silent ping mode...")
                silent_mode = True

            # loop pings
            await asyncio.sleep(20)

    def update_timeout_time(self, channel_name):
        status.print_status("[TWITCH] Ignoring channel {0} for the next 12 hours..."
                            .format(channel_name.upper()))
        new_time = {channel_name.upper(): datetime.now() + timedelta(hours=12)}
        self.twitch_username_skip_list.update(new_time)
