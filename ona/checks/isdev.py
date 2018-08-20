from discord.ext import commands


def is_dev():
    async def predicate(ctx: commands.Context):
        return ctx.author.id in ctx.bot.devs

    return commands.check(predicate)
