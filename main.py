from asyncio import get_event_loop
from ona.bot import bot

if __name__ == '__main__':
    loop = get_event_loop()
    loop.run_until_complete(bot.run())
    loop.close()
