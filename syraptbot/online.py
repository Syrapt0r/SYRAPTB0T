import asyncio
import requests
from random import randint
from syraptbot import status


# fetch the live status every five minutes
# THIS IS A VERY NAIVE APPROACH. THIS SHOULD BE SWITCHED TO WEBHOOK ASAP

async def test_livestream(bot, twitch_token, live_messages):
    await bot.wait_until_ready()

    message_posted = False

    while not bot.is_closed():
        if message_posted is False:
            status.print_status("Running Twitch live test...")

        skip_ping = False

        try:
            r = requests.get("https://api.twitch.tv/helix/streams?user_login=syrapt0r",
                             headers={"client-id": twitch_token})
            json_request = r.json()

        except requests.ConnectionError:
            status.print_status("Unable to fetch live status, skipping ping...")
            skip_ping = True
            json_request = {}

        if not skip_ping:
            if not json_request["data"]:
                if message_posted is False:
                    status.print_status("Twitch Channel appears to be offline. Entering silent ping mode...")
                    message_posted = True

                next_check_time = 300

            else:
                status.print_status("Twitch Channel is live!")
                message_posted = False

                # send notification to general
                for channel in bot.get_guild(473830853127176193).channels:
                    if channel.name.endswith("general"):
                        status.print_status("Found general channel, posting live message...")

                        rand_streem_nr = randint(0, len(live_messages) - 1)
                        await channel.send(live_messages[rand_streem_nr])
                        break

                # 8h timeout
                next_check_time = 28800
        else:
            next_check_time = 300

        await asyncio.sleep(next_check_time)
