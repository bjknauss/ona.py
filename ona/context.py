from discord.ext import commands


class Context(commands.Context):
    '''Custom context that adds a few things to make things easier.'''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def db(self):
        return self.bot.db
