from discord.ext import commands
from ona.bot import OnaBot, Context
from pymongo.collection import Collection
from ona.checks.isdev import is_dev


class TestCog:
    def __init__(self, bot: OnaBot):
        self.bot = bot
        if self.table.count() == 0:
            self.table.insert_one({'message': "test message", 'count': 5})

    @property
    def db(self):
        return self.bot.db

    @property
    def table(self) -> Collection:
        return self.db.test

    @commands.command()
    async def count(self, ctx: Context):
        doc = self.table.find_one()
        if doc:
            await ctx.send(str(doc.get('count', 'No count found...')))
        else:
            await ctx.send('No documents found.')

    @commands.command()
    async def inc(self, ctx: Context, amount: int = 1):
        result = self.table.update_one({}, {'$inc': {'count': amount}})
        if result.modified_count == 1:
            await ctx.send('Amount incremented.')
        else:
            await ctx.send('Failed to increment!')

    @commands.command()
    @is_dev()
    async def devping(self, ctx: Context):
        await ctx.send('pong!')


def setup(bot: OnaBot):
    bot.add_cog(TestCog(bot))
