import configparser
import datetime
from random import randint

from discord.ext import commands


def print_status(message):
    print(str(datetime.datetime.now()) + ': ' + message)


def main():
    # read config
    print_status('Loading bot token...')

    configParser = configparser.RawConfigParser()
    configFile = r'token.txt'
    configParser.read(configFile)

    print_status('Bot token loaded.')

    # some constants
    ROLE_ADMIN = "BIG GAY"
    ROLE_MOD_SUPER = "SUPERMODS OF DOOM"
    ROLE_MOD_NORMAL = "MODS OF DOOM"

    # 8ball answers
    ballAnswers = ["It is certain", "Without a doubt", "You may rely on it", "Yes definitely",
                   "It is decidedly so", "As I see it, yes", "Most likely", "Yes", "Outlook good",
                   "Signs point to yes", "Reply hazy try again", "Better not tell you now", "Ask again later",
                   "Cannot predict now", "Concentrate and ask again", "Don’t count on it", "Outlook not so good",
                   "My sources say no", "Very doubtful", "My reply is no"]
    print_status('Loaded {0} eightball answers'.format(len(ballAnswers)))

    # thankings
    thankYous = ["You're welcome", "<3", "No u", "aw stop", "nawww", ":3", "No prob", "Happy to help", "^-^"]
    print_status('Loaded {0} thanking answers'.format(len(thankYous)))

    # blacklisted channels
    channelBlacklist = [473830853127176197, 473872015279783976, 473878623229575178, 633315876757831690,
                        618472969735241759, 635260211178897419, 473877321711878175]
    print_status('Loaded {0} blacklisted channels'.format(len(channelBlacklist)))

    # get bot instance
    bot = commands.Bot(command_prefix='>')

    print_status('Bot connected!')

    # register bot commands
    @bot.command()
    async def shutdown(ctx):
        if ctx.message.channel.id not in channelBlacklist:
            if ROLE_ADMIN in [y.name.upper() for y in ctx.message.author.roles]:
                print_status('Bot disconnecting...')
                await ctx.send('ok bye ._.')
                await bot.close()
                exit(0)
            else:
                print_status('Got shutdown command from user with insufficient permissions')
                await ctx.send("You don't have the power to stop me, fool")
        else:
            print_status('Tried to call command in blacklisted channel, ignoring...')

    @bot.command()
    async def eightball(ctx):
        if ctx.message.channel.id not in channelBlacklist:
            print_status("{0} requested eight ball...".format(ctx.message.author.name))
            answer = randint(0, len(ballAnswers) - 1)
            print_status("Eight ball rolled {0}".format(str(answer)))

            await ctx.send(ballAnswers[answer])
        else:
            print_status('Tried to call command in blacklisted channel, ignoring...')

    @bot.command()
    async def random(ctx, *args):
        if ctx.message.channel.id not in channelBlacklist:
            print_status("{0} requested random number...".format(ctx.message.author.name))
            try:
                if len(args) == 0:
                    print_status("[RANDOM] no parameters, running default roll...")

                    await ctx.send("No range given, defaulting to 0 - 100...")
                    answer = randint(0, 100)
                    await ctx.send("Random number: {0}".format(str(answer)))
                elif len(args) == 1:
                    print_status("[RANDOM] 1 parameter, running roll...")

                    answer = randint(0, int(args[0]))
                    await ctx.send("Random number: {0}".format(str(answer)))
                elif len(args) == 2:
                    print_status("[RANDOM] 2 parameters, running roll...")

                    int1 = int(args[0])
                    int2 = int(args[1])

                    if int1 > int2:
                        int1, int2 = int2, int1

                    answer = randint(int1, int2)
                    await ctx.send("Random number: {0}".format(str(answer)))
                else:
                    print_status("[RANDOM] too many parameters, aborting...")
                    await ctx.send("Please only supply a maximum of two numbers. Thank")

            except TypeError:
                await ctx.send("One of your numbers is not even a number. What the hell are you doing.")
            except ValueError:
                await ctx.send("One of your numbers is not even a number. What the hell are you doing.")

        else:
            print_status('Tried to call command in blacklisted channel, ignoring...')

    @bot.command()
    async def thanks(ctx):
        if ctx.message.channel.id not in channelBlacklist:
            print_status("{0} said thanks :3".format(ctx.message.author.name))
            answer = randint(0, len(thankYous) - 1)
            print_status("Thank you message: {0}".format(str(answer)))

            await ctx.send(thankYous[answer])
        else:
            print_status('Tried to call command in blacklisted channel, ignoring...')

    # run bot with token
    token = configParser.get('token', 'token')
    bot.run(token)


if __name__ == "__main__":
    VERSION = "0.4"
    CURRENT_YEAR = "2019"
    AUTHOR = "SYRAPT0R"

    print_status('LAUNCHING SYRAPTB0T {0}, (c) {1} {2}'.format(VERSION, CURRENT_YEAR, AUTHOR))
    main()
