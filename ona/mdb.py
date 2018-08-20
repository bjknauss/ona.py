import pymongo
from .config.dbcl import DatabaseConfig


class Database(DatabaseConfig):
    '''Class responsible for loading the DB config and connecting to client.'''

    def __init__(self):
        super().__init__()
        self._client = pymongo.MongoClient(host=self.host, port=self.port)
        self._db = self.client[self.dbname]

    @property
    def client(self) -> pymongo.mongo_client.MongoClient:
        return self._client

    @property
    def db(self) -> pymongo.database.Database:
        return self._db
