import asyncio
import requests
from random import randint
from syraptbot import status


# fetch the live status every five minutes
# THIS IS A VERY NAIVE APPROACH. THIS SHOULD BE SWITCHED TO WEBHOOK ASAP

async def testLivestream(bot, TWITCH_TOKEN, liveMessages):
    await bot.wait_until_ready()

    messagePosted = False

    while not bot.is_closed():
        if messagePosted is False:
            status.print_status("Running Twitch live test...")

        r = requests.get("https://api.twitch.tv/helix/streams?user_login=syrapt0r",
                         headers={"client-id": TWITCH_TOKEN})
        jsonR = r.json()

        if not jsonR["data"]:
            if messagePosted is False:
                status.print_status("Twitch Channel appears to be offline. Entering silent ping mode...")
                messagePosted = True

            nextCheckTime = 300

        else:
            status.print_status("Twitch Channel is live!")
            messagePosted = False

            # send notification to general
            for channel in bot.get_guild(473830853127176193).channels:
                if channel.name.endswith("general"):
                    status.print_status("Found general channel, posting live message...")

                    randStremNr = randint(0, len(liveMessages) - 1)
                    await channel.send(liveMessages[randStremNr])
                    break

            # 8h timeout
            nextCheckTime = 28800

        await asyncio.sleep(nextCheckTime)
