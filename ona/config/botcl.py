from .bcl import BaseConfigLoader

default_description = 'A bot made for fun.'


class BotConfig(BaseConfigLoader):
    def __init__(self, filename='bot.yml'):
        print(f'filename: {filename}')
        super().__init__(filename)

    @property
    def token(self) -> str:
        return self.raw_cfg.get('token')

    @property
    def devs(self) -> list:
        return self.raw_cfg.get('devs', [])

    @property
    def command_prefix(self) -> str:
        return self.raw_cfg.get('command_prefix', '.')

    @property
    def description(self) -> str:
        return self.raw_cfg.get('description', default_description)

    @property
    def cogs(self) -> list:
        return self.raw_cfg.get('cogs', [])
