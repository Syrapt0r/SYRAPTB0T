from os.path import isfile

from discord.ext import commands

from syraptbot import perms, status, fileOperations, online, botCommands


def main():
    # load bot token
    status.print_status('Loading config...')
    config_data = fileOperations.read_config_file()

    status.print_status('Config file loaded.')

    # check that we have a discord token
    if config_data["token_discord"] is "":
        status.print_status("No Discord token specified, aborting...")
        exit(0)

    status.print_status("Discord token loaded.")

    twitch_enabled = True

    # twitch token
    twitch_token = ""
    twitch_username = ""

    if config_data["token_twitch"] is "" or config_data["twitch_username"] is "":
        twitch_enabled = False

    if twitch_enabled:
        twitch_token = config_data["token_twitch"]
        twitch_username = config_data["twitch_username"]

        status.print_status('Twitch token loaded.')

    # initialize blacklisted channels
    channel_blacklist = fileOperations.read_file("files/channelBlacklist.txt")
    status.print_status('Loaded {0} blacklisted channels'.format(len(channel_blacklist)))

    # set up bot instance
    bot = commands.Bot(command_prefix='>')

    # register bot commands
    @bot.command(help='Closes the bot. Only callable by admins.')
    async def shutdown(ctx):
        if perms.channel_permitted(ctx, channel_blacklist):
            await botCommands.shutdown(bot, ctx)

    @bot.command(help='Gives a random eight ball answer')
    async def eightball(ctx, *args):
        if perms.channel_permitted(ctx, channel_blacklist):
            await botCommands.eightball(ctx, args)

    @bot.command(help='Generates a random number between 0 and 100 (if no parameters are given), 0 to x (if one'
                      ' parameter is given) or x and y (if two parameters are given)')
    async def random(ctx, *args):
        if perms.channel_permitted(ctx, channel_blacklist):
            await botCommands.random(ctx, *args)

    @bot.command(help='Make sure to thank your bot')
    async def thanks(ctx):
        if perms.channel_permitted(ctx, channel_blacklist):
            await botCommands.thanks(ctx)

    @bot.command(help='Generates a random joke using advanced AI')
    async def joke(ctx):
        if perms.channel_permitted(ctx, channel_blacklist):
            await botCommands.joke(ctx)

    @bot.command(help='Outputs stats about bot usage')
    async def stats(ctx):
        if perms.channel_permitted(ctx, channel_blacklist):
            await botCommands.stats(ctx)

    @bot.command(help='Outputs an invite link')
    async def invite(ctx):
        if perms.channel_permitted(ctx, channel_blacklist):
            await ctx.send("https://discordapp.com/invite/JWhvAFW")

    @bot.command(help='ribs')
    async def ribs(ctx):
        if perms.channel_permitted(ctx, channel_blacklist):
            await botCommands.ribs(ctx)

    @bot.command(help='Rolls a set amount of virtual dice')
    async def roll(ctx, arg):
        if perms.channel_permitted(ctx, channel_blacklist):
            await botCommands.roll(ctx, arg)

    # run twitch connection test thread
    if twitch_enabled:
        bot.loop.create_task(online.test_livestream(bot, twitch_token, twitch_username))

    else:
        status.print_status("Disabled twitch test.")

    # run bot with token
    status.print_status('Bot connected!')
    bot.run(config_data["token_discord"])


if __name__ == "__main__":
    # define some variables
    VERSION = "0.14"
    COPYRIGHT_YEAR = "2019-2020"
    AUTHOR = "SYRAPT0R"

    # make sure a config exists
    if not isfile("config.txt"):
        fileOperations.generate_default_config()
        exit(0)

    status.print_status('LAUNCHING SYRAPTB0T {0}, (c) {1} {2}'.format(VERSION, COPYRIGHT_YEAR, AUTHOR))

    # start main loop
    main()
