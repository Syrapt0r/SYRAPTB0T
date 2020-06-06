from os.path import isfile

from discord.ext import commands

from syraptbot import perms, status, fileOperations, twitch, botCommands


def main():
    # load bot token
    status.print_status('[MAIN] Loading config...')
    config_data = fileOperations.read_config_file()

    status.print_status('[MAIN] Config file loaded.')

    # check that we have a discord token
    if config_data["token_discord"] is "":
        status.print_status("[MAIN] No Discord token specified, aborting...")
        exit(0)

    discord_guild = config_data["guild_discord"]
    status.print_status("Discord token loaded.")

    twitch_enabled = True

    # twitch token
    twitch_c_id = ""
    twitch_c_secret = ""
    twitch_usernames = ""

    if config_data["twitch_client_id"] is "" or config_data["twitch_usernames"] is "":
        twitch_enabled = False

    if twitch_enabled:
        twitch_c_id = config_data["twitch_client_id"]
        twitch_c_secret = config_data["twitch_client_secret"]

        twitch_usernames = config_data["twitch_usernames"]

        status.print_status('[MAIN] Twitch data loaded.')

    # initialize blacklisted channels
    channel_blacklist = fileOperations.read_file("files/channelBlacklist.txt")
    status.print_status('[MAIN] Loaded {0} blacklisted channels'.format(len(channel_blacklist)))

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
        twitch_api = twitch.TwitchAPI(bot, twitch_c_id, twitch_c_secret, twitch_usernames, discord_guild)
        bot.loop.create_task(twitch_api.check_twitch_channels(bot))

    else:
        status.print_status("[MAIN] Disabled twitch test.")

    # run bot with token
    status.print_status('[MAIN] Bot connected!')
    bot.run(config_data["token_discord"])


if __name__ == "__main__":
    # define some variables
    VERSION = "0.15.1"
    COPYRIGHT_YEAR = "2019-2020"
    AUTHOR = "SYRAPT0R"

    # make sure a config exists
    if not isfile("config.txt"):
        fileOperations.generate_default_config()
        exit(0)

    status.print_status('#### LAUNCHING SYRAPTB0T {0}, (c) {1} {2} ####'.format(VERSION, COPYRIGHT_YEAR, AUTHOR))

    # start main loop
    main()
