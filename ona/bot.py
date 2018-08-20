from discord.ext import commands
from .config.botcl import BotConfig
from .mdb import Database
from .context import Context
from .checks.isdev import is_dev
import sys, traceback


class OnaBot(commands.Bot):
    '''Custom bot that inherits from the discord.py bot.'''

    def __init__(self, *args, **kwargs):
        self.cfg = BotConfig()
        super().__init__(command_prefix=self.cfg.command_prefix, pm_help=True)
        self._mdb = Database()
        self.add_command(self.ping)
        self.add_command(self.reload)
        for extension in self.cfg.cogs:
            try:
                self.load_extension(extension)
            except Exception as e:
                traceback.print_exc()
                print(
                    f'Failed to load extension {extension}.', file=sys.stderr)

    @property
    def devs(self):
        return self.cfg.devs

    @property
    def db(self):
        '''Returns the current mongo db.'''
        return self._mdb.db

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)
        await self.invoke(ctx)

    @commands.command()
    @is_dev()
    async def reload(self, ctx: Context):
        for ext in self.cfg.cogs:
            try:
                self.unload_extension(ext)
                self.load_extension(ext)
            except Exception as e:
                print(f'An error occured reloading the {ext} extension.')
                traceback.print_exc(file=sys.stderr)
                await ctx.send(f'Extension {ext} failed to reload!')
            else:
                await ctx.send(f'{len(self.cfg.cogs)} cogs reloaded!')

    @commands.command()
    async def ping(self, ctx: Context):
        await ctx.send('pong!')

    def run(self):
        super().run(self.cfg.token)


bot = OnaBot()
