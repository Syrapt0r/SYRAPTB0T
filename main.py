import configparser
import datetime

from discord.ext import commands


def print_status(message):
    print(str(datetime.datetime.now()) + ': ' + message)


def main():
    # read config
    configParser = configparser.RawConfigParser()
    configFile = r'token.txt'
    configParser.read(configFile)

    # get bot instance
    bot = commands.Bot(command_prefix='>')

    print_status('Bot connected!')

    # register bot commands
    @bot.command()
    async def disconnect(ctx):
        if "SYRAPT0R" in [y.name.upper() for y in ctx.message.author.roles]:
            print_status('Bot disconnecting...')
            await ctx.send('ok bye ._.')
            await bot.close()
            exit(0)
        else:
            print_status('Got shutdown command from user with insufficient permissions')
            await ctx.send("You don't have the power to stop me, fool")

    @bot.command()
    async def ban(ctx):
        if "SYRAPT0R" in [y.name.upper() for y in ctx.message.author.roles] or "SUPERMODS OF DOOM" in [y.name.upper()
                                                                                                       for y in
                                                                                                       ctx.message.author.roles]:
            userToBan = ctx.message.mentions[0]
            print_status("DEBUG: Mention was {0}".format(str(userToBan)))
            if ctx.message.mentions[0] == bot.user:
                print_status('User tried to ban the bot, ignoring')
                await ctx.send("You can't ban me, fool")
                return
        else:
            print_status('User tried to use ban with insufficient permissions')
            await ctx.send("You don't have permission to use this command")

    # run bot with token
    token = configParser.get('token', 'token')
    bot.run(token)


if __name__ == "__main__":
    print_status('LAUNCHING SYRAPTB0T 0.1, (c) 2019 SYRAPT0R')
    main()
