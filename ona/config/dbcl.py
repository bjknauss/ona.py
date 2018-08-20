from .bcl import BaseConfigLoader


class DatabaseConfig(BaseConfigLoader):
    def __init__(self, filename='db.yml'):
        super().__init__(filename)

    @property
    def host(self):
        return self.raw_cfg.get('host', 'localhost')

    @property
    def port(self):
        return self.raw_cfg.get('port', 27017)

    @property
    def dbname(self):
        return self.raw_cfg.get('dbname', 'onapy')
