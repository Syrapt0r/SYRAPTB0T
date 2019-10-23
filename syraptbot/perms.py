def checkPermissions(roles, author):
    for role in roles:
        if role in [y.name.upper() for y in author.roles]:
            return True

    return False
