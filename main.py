from datetime import datetime, timedelta
from os import walk, path
from random import randint

from discord import File
from discord.ext import commands

from syraptbot import perms, status, fileOperations


def main():
    # read config
    status.print_status('Loading bot token...')

    token = fileOperations.readToken()
    if token is None:
        status.print_status("Token file not found.\nMake sure the file token.txt exists in the same folder as this "
                            "script.")
        exit(0)

    status.print_status('Bot token loaded.')

    # load stats
    if path.exists("stats.txt"):
        statistics = fileOperations.loadStats()
        status.print_status("Stats loaded successfully.")
    else:
        statistics = {"eightballs": 0, "jokes": 0, "randoms": 0, "thanks": 0, "stats": 0, "ribs": 0}
        fileOperations.saveStats(statistics)
        status.print_status("No previous stats found, initiated new stats.")

    # some constants
    ROLE_ADMIN = "BIG GAY"
    ROLE_MOD_SUPER = "SUPERMODS OF DOOM"

    # get ribs
    ribPictures = []
    for (dirpath, dirnames, filenames) in walk("ribs"):
        ribPictures.extend(filenames)
        break

    status.print_status('Loaded {0} rib pictures'.format(len(ribPictures)))

    # init timeout
    ribTimeout = {}
    ribTimeoutInterval = 300

    # 8ball answers
    ballAnswers = ["It is certain", "Without a doubt", "You may rely on it", "Yes definitely",
                   "It is decidedly so", "As I see it, yes", "Most likely", "Yes", "Outlook good",
                   "Signs point to yes", "Reply hazy try again", "Better not tell you now", "Ask again later",
                   "Cannot predict now", "Concentrate and ask again", "Don’t count on it", "Outlook not so good",
                   "My sources say no", "Very doubtful", "My reply is no", "Lol nope", "Hah you wish",
                   "Okay but only once", "Fiiine", "Count to 10 and ask again", "Why would I know that", "what",
                   "If you dare ask me that again I will ban you", "no u", "Sure thing bro",
                   "Hm? Sorry, wasn't listening"]
    status.print_status('Loaded {0} eightball answers'.format(len(ballAnswers)))

    # joke setup
    jokeBegin = ["So a ", "A ", "So this ", "This ", "Uh, this ", "A singular ", "The "]
    jokePeople = ["man ", "woman ", "child ", "horse ", "car ", "bird ", "skeleton ", "fairy ", "dragon ", "rib ",
                  "huge dude ", "big man ", "person ", "kid ", "dude ", "cowboy ", "sheriff ", "boat ", "Mario ",
                  "Waluigi ", "ice cream man ", "Dr. Pepper can ", "mailman ", "cricket player ", "baby ", "dog",
                  "cat ", "spaceship ", "hand "]
    jokeAction = ["goes into ", "crashes into ", "walks to ", "gets to ", "eats ", "finds ", "runs from ",
                  "screams at ", "stumbles upon ", "looks at ", "arrives at ", "buys ", "exits ", "shoots ",
                  "rams into ", "360 noscopes ", "gazes at ", "inhales "]
    jokeLocation = ["a bar. ", "a mall. ", "a playground. ", "a cinema. ", "a beach. ", "a parking lot. ",
                    "an ice cream van. ", "a shop. ", "a ship. ", "a toilet. ", "a bear. ", "a penguin. ", "a man. ",
                    "a woman. ", "a skeleton. ", "a dog. ", "the USS Enterprise. ", "a smartphone. ", "an asteroid. ",
                    "five children. ", "a truck. ", "Mario. ", "Luigi. ", "Wario. ", "Waluigi. "]
    jokeTwist = ["Suddenly, a ", "Then, a ", "After that, a ", "But then a ", "Later, a ", "But suddenly a ",
                 "However, then a "]
    jokePunchline = ["screams 'I am gay'", "screams 'Joe Mama'", "types 'ribs'", "explodes", "catches fire", "dies",
                     "becomes a zombie", "yeets", "is your mom", "is your dad", "was you all along", "eats a pie",
                     "dabs", "implodes", "plays Mario Kart", "drinks some bleach", "comes back to life"]

    jokeBeginCount = len(jokeBegin) - 1
    jokePeopleCount = len(jokePeople) - 1
    jokeActionCount = len(jokeAction) - 1
    jokeLocationCount = len(jokeLocation) - 1
    jokeTwistCount = len(jokeTwist) - 1
    jokePunchlineCount = len(jokePunchline) - 1

    # thankings
    thankYous = ["You're welcome", "No u", "aw stop", "nawww", ":3", "No prob", "Happy to help", "^-^",
                 "stahp it", "Thanks :3", "Just doing my best c:", "no thank YOU", "It's my duty ^-^",
                 "ᶦ ᵈᶦᵈⁿᵗ ʰᵃᵛᵉ ᵃ ᶜʰᵒᶦᶜᵉ I mean thanks ^-^"]
    status.print_status('Loaded {0} thanking answers'.format(len(thankYous)))

    # blacklisted channels
    channelBlacklist = [473830853127176197, 473872015279783976, 473878623229575178, 633315876757831690,
                        618472969735241759, 635260211178897419, 473877321711878175]
    status.print_status('Loaded {0} blacklisted channels'.format(len(channelBlacklist)))

    # get bot instance
    bot = commands.Bot(command_prefix='>')
    status.print_status('Bot connected!')

    # register bot commands
    @bot.command(help='Closes the bot. Only callable by admins.')
    async def shutdown(ctx):
        if ctx.message.channel.id in channelBlacklist:
            status.print_status('Tried to call command in blacklisted channel, ignoring...')
            return

        if perms.checkPermissions([ROLE_ADMIN, ROLE_MOD_SUPER], ctx.message.author):
            status.print_status('Bot disconnecting...')
            fileOperations.saveStats(statistics)
            await ctx.send('ok bye ._.')
            await bot.close()
            exit(0)
        else:
            status.print_status('Got shutdown command from user with insufficient permissions')
            await ctx.send("You don't have the power to stop me, fool")

    @bot.command(help='Gives a random eight ball answer')
    async def eightball(ctx):
        if ctx.message.channel.id in channelBlacklist:
            status.print_status('Tried to call command in blacklisted channel, ignoring...')
            return

        status.print_status("{0} requested eight ball...".format(ctx.message.author.name))
        statistics["eightballs"] = statistics["eightballs"] + 1

        answer = randint(0, len(ballAnswers) - 1)
        status.print_status("Eight ball rolled {0}".format(str(answer)))

        await ctx.send(ballAnswers[answer])

    @bot.command(help='Generates a random number between 0 and 100 (if no parameters are given), 0 to x (if one'
                      ' parameter is given) or x and y (if two parameters are given)')
    async def random(ctx, *args):
        if ctx.message.channel.id in channelBlacklist:
            status.print_status('Tried to call command in blacklisted channel, ignoring...')
            return

        status.print_status("{0} requested random number...".format(ctx.message.author.name))
        statistics["randoms"] = statistics["randoms"] + 1

        try:
            if len(args) == 0:
                status.print_status("[RANDOM] no parameters, running default roll...")

                await ctx.send("No range given, defaulting to 0 - 100...")
                answer = randint(0, 100)
                await ctx.send("Random number: {0}".format(str(answer)))

            elif len(args) == 1:
                status.print_status("[RANDOM] 1 parameter, running roll...")

                answer = randint(0, int(args[0]))
                await ctx.send("Random number: {0}".format(str(answer)))

            elif len(args) == 2:
                status.print_status("[RANDOM] 2 parameters, running roll...")

                int1 = int(args[0])
                int2 = int(args[1])
                if int1 > int2:
                    int1, int2 = int2, int1
                answer = randint(int1, int2)
                await ctx.send("Random number: {0}".format(str(answer)))

            else:
                status.print_status("[RANDOM] too many parameters, aborting...")
                await ctx.send("Please only supply a maximum of two numbers. Thank")

        except TypeError:
            await ctx.send("One of your numbers is not even a number. What the hell are you doing.")
        except ValueError:
            await ctx.send("One of your numbers is not even a number. What the hell are you doing.")

    @bot.command(help='Make sure to thank your bot')
    async def thanks(ctx):
        if ctx.message.channel.id in channelBlacklist:
            status.print_status('Tried to call command in blacklisted channel, ignoring...')
            return

        status.print_status("{0} said thanks :3".format(ctx.message.author.name))
        statistics["thanks"] = statistics["thanks"] + 1

        answer = randint(0, len(thankYous) - 1)
        status.print_status("Thank you message: {0}".format(str(answer)))

        await ctx.send(thankYous[answer])

    @bot.command(help='Generates a random joke using advanced AI')
    async def joke(ctx):
        if ctx.message.channel.id in channelBlacklist:
            status.print_status('Tried to call command in blacklisted channel, ignoring...')
            return

        status.print_status("{0} requested joke".format(ctx.message.author.name))
        statistics["jokes"] = statistics["jokes"] + 1

        begin = randint(0, jokeBeginCount)
        person1 = randint(0, jokePeopleCount)
        action = randint(0, jokeActionCount)
        location = randint(0, jokeLocationCount)
        twist = randint(0, jokeTwistCount)
        person2 = randint(0, jokePeopleCount)
        punchline = randint(0, jokePunchlineCount)

        await ctx.send(
            '' + jokeBegin[begin] + jokePeople[person1] + jokeAction[action] + jokeLocation[location] + jokeTwist[
                twist] + jokePeople[person2] + jokePunchline[punchline])

    @bot.command(help='Outputs stats about bot usage')
    async def stats(ctx):
        if ctx.message.channel.id in channelBlacklist:
            status.print_status('Tried to call command in blacklisted channel, ignoring...')
            return

        status.print_status("{0} requested stats".format(ctx.message.author.name))
        statistics["stats"] = statistics["stats"] + 1

        await ctx.send(
            'So far, the bot has given {0} eightball answers, has generated {1} random numbers, sent {2} ribs and '
            'told {3} jokes. It has been thanked {4} times.'.format(str(statistics["eightballs"]),
                                                                    str(statistics["randoms"]),
                                                                    str(statistics["ribs"]),
                                                                    str(statistics["jokes"]),
                                                                    str(statistics["thanks"])))

    @bot.command(help='Outputs an invite link')
    async def invite(ctx):
        if ctx.message.channel.id in channelBlacklist:
            status.print_status('Tried to call command in blacklisted channel, ignoring...')
            return

        await ctx.send("https://discordapp.com/invite/JWhvAFW")

    @bot.command(help='ribs')
    async def ribs(ctx):
        if ctx.message.channel.id in channelBlacklist:
            status.print_status('Tried to call command in blacklisted channel, ignoring...')
            return

        status.print_status("{0} requested ribs".format(ctx.message.author.name))

        if ctx.message.author.id not in ribTimeout:
            ribTimeout[ctx.message.author.id] = datetime.now()

            ribNr = randint(0, len(ribPictures) - 1)
            await ctx.message.channel.send(file=File(r"ribs/" + ribPictures[ribNr]))

            statistics["ribs"] = statistics["ribs"] + 1
            return

        compareTime = ribTimeout[ctx.message.author.id] + timedelta(seconds=ribTimeoutInterval)

        if datetime.now() > compareTime:
            statistics["ribs"] = statistics["ribs"] + 1

            ribTimeout[ctx.message.author.id] = datetime.now()
            ribNr = randint(0, len(ribPictures) - 1)
            await ctx.message.channel.send(file=File(r"ribs/" + ribPictures[ribNr]))
        else:
            status.print_status('User is currently in timeout')
            await ctx.send("Don't spam the rib")

    # run bot with token
    bot.run(token)


if __name__ == "__main__":
    VERSION = "0.9.2"
    COPYRIGHT_YEAR = "2019"
    AUTHOR = "SYRAPT0R"

    status.print_status('LAUNCHING SYRAPTB0T {0}, (c) {1} {2}'.format(VERSION, COPYRIGHT_YEAR, AUTHOR))
    main()
