import re
from datetime import datetime, timedelta
from os import path, walk
from random import randint

from discord import File

from syraptbot import status, perms, fileOperations

# load statistics
if path.exists("stats.txt"):
    statistics = fileOperations.load_stats()

    if statistics == "STAT_LOAD_ERROR":
        status.print_status("Error loading statistics. Make sure the statistic file is not malformed.")
        exit(0)

    status.print_status("Stats loaded successfully.")
else:
    statistics = {"eightballs": 0, "jokes": 0, "randoms": 0, "thanks": 0, "stats": 0, "ribs": 0, "rolls": 0}
    fileOperations.save_stats(statistics)
    status.print_status("No previous stats found, initiated new stats.")

# define some constants
role_admin = "BIG GAY"
role_mod_super = "SUPERMODS OF DOOM"

# epic regex
not_empty = "[_*A-Za-z0-9?!.,:]"
not_empty_r = re.compile(not_empty)

# load rib picture paths
rib_pictures = []
for (dirpath, dirnames, filenames) in walk("ribs"):
    rib_pictures.extend(filenames)
    break

rib_timeout = []
rib_timeout_interval = 300

status.print_status('Loaded {0} rib pictures'.format(len(rib_pictures)))

# define 8ball answers
ball_answers = fileOperations.read_file("files/eightball.txt")
ball_answers_empty = fileOperations.read_file("files/eightballEmpty.txt")

status.print_status('Loaded {0} eightball answers'.format(len(ball_answers)))
status.print_status('Loaded {0} empty eightball answers'.format(len(ball_answers_empty)))

# define bot thank responses
thank_yous = fileOperations.read_file("files/thanks.txt")
status.print_status('Loaded {0} thanking answers'.format(len(thank_yous)))


async def shutdown(bot, ctx):
    if perms.check_permissions([role_admin, role_mod_super], ctx.message.author):
        status.print_status('SHUTDOWN...')
        fileOperations.save_stats(statistics)

        await ctx.send('ok bye ._.')

        status.print_status('Bot disconnecting...')
        await bot.close()
    else:
        status.print_status('Got shutdown command from user with insufficient permissions')
        await ctx.send("You don't have the power to stop me, fool")


async def eightball(ctx, args):
    status.print_status("{0} requested eight ball...".format(ctx.message.author.name))
    statistics["eightballs"] = statistics["eightballs"] + 1

    if len(args) == 0:
        answer = randint(0, len(ball_answers_empty) - 1)
        await ctx.send(ball_answers_empty[answer])

        status.print_status("No question, eight ball rolled {0}".format(str(answer)))
    else:
        if not_empty_r.match(args[0]):
            answer = randint(0, len(ball_answers) - 1)
            await ctx.send(ball_answers[answer])

            status.print_status("Eight ball rolled {0}".format(str(answer)))

        else:
            answer = randint(0, len(ball_answers_empty) - 1)
            await ctx.send(ball_answers_empty[answer])

            status.print_status("Empty queue, NICE TRY MATE")


async def random(ctx, args):
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


async def thanks(ctx):
    status.print_status("{0} said thanks :3".format(ctx.message.author.name))
    statistics["thanks"] = statistics["thanks"] + 1

    answer = randint(0, len(thank_yous) - 1)
    status.print_status("Thank you message: {0}".format(str(answer)))

    await ctx.send(thank_yous[answer])


# define joke parts
joke_begin = ["So a ", "A ", "So this ", "This ", "Uh, this ", "A singular ", "The "]
joke_people = ["man ", "woman ", "child ", "horse ", "car ", "bird ", "skeleton ", "fairy ", "dragon ", "rib ",
               "huge dude ", "big man ", "person ", "kid ", "dude ", "cowboy ", "sheriff ", "boat ", "Mario ",
               "Waluigi ", "ice cream man ", "Dr. Pepper can ", "mailman ", "cricket player ", "baby ", "dog",
               "cat ", "spaceship ", "hand "]
joke_action = ["goes into ", "crashes into ", "walks to ", "gets to ", "eats ", "finds ", "runs from ",
               "screams at ", "stumbles upon ", "looks at ", "arrives at ", "buys ", "exits ", "shoots ",
               "rams into ", "360 noscopes ", "gazes at ", "inhales "]
joke_location = ["a bar. ", "a mall. ", "a playground. ", "a cinema. ", "a beach. ", "a parking lot. ",
                 "an ice cream van. ", "a shop. ", "a ship. ", "a toilet. ", "a bear. ", "a penguin. ", "a man. ",
                 "a woman. ", "a skeleton. ", "a dog. ", "the USS Enterprise. ", "a smartphone. ", "an asteroid. ",
                 "five children. ", "a truck. ", "Mario. ", "Luigi. ", "Wario. ", "Waluigi. "]
joke_twist = ["Suddenly, a ", "Then, a ", "After that, a ", "But then a ", "Later, a ", "But suddenly a ",
              "However, then a "]
joke_punchline = ["screams 'I am gay'", "screams 'Joe Mama'", "types 'ribs'", "explodes", "catches fire", "dies",
                  "becomes a zombie", "yeets", "is your mom", "is your dad", "was you all along", "eats a pie",
                  "dabs", "implodes", "plays Mario Kart", "drinks some bleach", "comes back to life"]

joke_begin_count = len(joke_begin) - 1
joke_people_count = len(joke_people) - 1
joke_action_count = len(joke_action) - 1
joke_location_count = len(joke_location) - 1
joke_twist_count = len(joke_twist) - 1
joke_punchline_count = len(joke_punchline) - 1


async def joke(ctx):
    status.print_status("{0} requested joke".format(ctx.message.author.name))
    statistics["jokes"] = statistics["jokes"] + 1

    begin = randint(0, joke_begin_count)
    person1 = randint(0, joke_people_count)
    action = randint(0, joke_action_count)
    location = randint(0, joke_location_count)
    twist = randint(0, joke_twist_count)
    person2 = randint(0, joke_people_count)
    punchline = randint(0, joke_punchline_count)

    await ctx.send(
        '' + joke_begin[begin] + joke_people[person1] + joke_action[action] + joke_location[location] + joke_twist[
            twist] + joke_people[person2] + joke_punchline[punchline])


async def stats(ctx):
    status.print_status("{0} requested stats".format(ctx.message.author.name))
    statistics["stats"] = statistics["stats"] + 1

    await ctx.send(
        'So far, the bot has given {0} eightball answers, has generated {1} random numbers, sent {2} ribs, '
        'told {3} jokes and rolled {4} dice. It has been thanked {5} times.'.format(str(statistics["eightballs"]),
                                                                                    str(statistics["randoms"]),
                                                                                    str(statistics["ribs"]),
                                                                                    str(statistics["jokes"]),
                                                                                    str(statistics["rolls"]),
                                                                                    str(statistics["thanks"])))


async def ribs(ctx):
    status.print_status("{0} requested ribs".format(ctx.message.author.name))
    statistics["ribs"] = statistics["ribs"] + 1

    if ctx.message.author.id not in rib_timeout:
        rib_timeout[ctx.message.author.id] = datetime.now()

        rib_nr = randint(0, len(rib_pictures) - 1)
        await ctx.message.channel.send(file=File(r"ribs/" + rib_pictures[rib_nr]))

        statistics["ribs"] = statistics["ribs"] + 1
        return

    compare_time = rib_timeout[ctx.message.author.id] + timedelta(seconds=rib_timeout_interval)

    if datetime.now() > compare_time:
        statistics["ribs"] = statistics["ribs"] + 1

        rib_timeout[ctx.message.author.id] = datetime.now()
        rib_nr = randint(0, len(rib_pictures) - 1)
        await ctx.message.channel.send(file=File(r"ribs/" + rib_pictures[rib_nr]))
    else:
        status.print_status('User is currently in timeout')
        await ctx.send("Don't spam the rib")


async def roll(ctx, arg):
    status.print_status("{0} requested roll".format(ctx.message.author.name))
    statistics["rolls"] = statistics["rolls"] + 1

    if arg is not None:
        roll_data = arg.split("d")

    else:
        await ctx.send("Invalid parameters. Make sure you provide one parameter in the form of \"[number of "
                       "rolls]d[type of dice]\"")
        return

    if len(roll_data) != 2:
        await ctx.send("Invalid parameters. Make sure you provide one parameter in the form of \"[number of "
                       "rolls]d[type of dice]\"")
        return

    try:
        rolls = int(roll_data[0])
        dice = int(roll_data[1])

    except TypeError:
        await ctx.send("You posted cringe bro")
        return

    except ValueError:
        await ctx.send("You posted cringe bro")
        return

    if rolls * dice > 10000:
        await ctx.send("Please choose lower parameters. What would you need this for anyway")
        return

    status.print_status("Rolling {0} {1}-sided dice".format(rolls, dice))

    roll_results = []
    total_result = 0

    for i in range(dice):
        roll_results.append(0)

    answer_str = "Rolls: "

    for current_roll in range(rolls):
        current_result = randint(1, dice)
        roll_results[current_result - 1] += 1

        total_result += current_result

        if answer_str != "Rolls: ":
            answer_str += ", "
        answer_str += str(current_result)

    count_str = "Counts: "

    for current_roll in range(dice):
        if roll_results[current_roll] != 0:
            if count_str != "Counts: ":
                count_str += ", "

            count_str += "{0} x {1}".format(roll_results[current_roll], current_roll + 1)

    await ctx.send(answer_str)

    if rolls != 1:
        await ctx.send(count_str)
        await ctx.send("Total: {0}".format(total_result))
