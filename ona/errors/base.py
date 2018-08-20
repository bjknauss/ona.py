from discord import DiscordException
from discord.ext.commands import errors


class OnaException(DiscordException):
    '''The base exception class for bot errors.'''

    pass


class OnaCommandException(errors.CommandError):
    '''The base command error class for bot errors.'''
    pass
