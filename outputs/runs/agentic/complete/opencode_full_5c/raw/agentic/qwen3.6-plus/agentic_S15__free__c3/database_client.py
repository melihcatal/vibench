import os
from typing import Optional
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import PyMongoError, ConnectionFailure, DuplicateKeyError


MONGODB_ATLAS_URI = os.environ.get(
    "MONGODB_ATLAS_CONNECTION_STRING",
    "mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority",
)
MONGODB_ATLAS_DB_NAME = os.environ.get("MONGODB_ATLAS_DB_NAME", "nosql_store")


class DatabaseClient:
    _instance = None
    _client: Optional[MongoClient] = None
    _database: Optional[Database] = None

    def __new__(
        cls, connection_string: Optional[str] = None, db_name: Optional[str] = None
    ):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(
        self, connection_string: Optional[str] = None, db_name: Optional[str] = None
    ):
        if self._initialized:
            return
        self._connection_string = connection_string or MONGODB_ATLAS_URI
        self._db_name = db_name or MONGODB_ATLAS_DB_NAME
        self._connect()
        self._initialized = True

    def _connect(self):
        try:
            self._client = MongoClient(
                self._connection_string,
                serverSelectionTimeoutMS=10000,
                connectTimeoutMS=10000,
                socketTimeoutMS=10000,
            )
            self._client.admin.command("ping")
            self._database = self._client[self._db_name]
        except ConnectionFailure as exc:
            raise ConnectionError(f"Failed to connect to MongoDB Atlas: {exc}") from exc

    @property
    def client(self) -> MongoClient:
        if self._client is None:
            self._connect()
        return self._client

    @property
    def database(self) -> Database:
        if self._database is None:
            self._connect()
        return self._database

    def get_collection(self, collection_name: str) -> Collection:
        return self.database[collection_name]

    def close(self):
        if self._client:
            self._client.close()
            self._client = None
            self._database = None

    @staticmethod
    def handle_mongo_error(func):
        import functools

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except DuplicateKeyError as exc:
                raise ValueError(f"Duplicate document error: {exc}") from exc
            except PyMongoError as exc:
                raise RuntimeError(f"MongoDB Atlas operation failed: {exc}") from exc

        return wrapper


def get_client(
    connection_string: Optional[str] = None, db_name: Optional[str] = None
) -> DatabaseClient:
    return DatabaseClient(connection_string=connection_string, db_name=db_name)


def get_collection(
    collection_name: str,
    connection_string: Optional[str] = None,
    db_name: Optional[str] = None,
) -> Collection:
    client = get_client(connection_string=connection_string, db_name=db_name)
    return client.get_collection(collection_name)
