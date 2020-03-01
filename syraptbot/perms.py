from syraptbot import status


def check_permissions(roles, author):
    for role in roles:
        if role.upper() in [y.name.upper() for y in author.roles]:
            return True

    return False


def channel_permitted(ctx, channel_blacklist):
    if ctx.message.channel.id in channel_blacklist:
        status.print_status('Tried to call command in blacklisted channel, ignoring...')
        return False

    return True
