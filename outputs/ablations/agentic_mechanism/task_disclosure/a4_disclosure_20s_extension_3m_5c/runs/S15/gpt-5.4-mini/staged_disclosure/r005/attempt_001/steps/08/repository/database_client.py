import os
from functools import lru_cache

from azure.cosmos import CosmosClient, PartitionKey


DEFAULT_ENDPOINT = os.getenv("COSMOS_DB_ENDPOINT", "")
DEFAULT_KEY = os.getenv("COSMOS_DB_KEY", "")
DEFAULT_DATABASE = os.getenv("COSMOS_DB_DATABASE", "appdb")
DEFAULT_CONTAINER = os.getenv("COSMOS_DB_CONTAINER", "items")


class DatabaseConfig:
    def __init__(self, endpoint: str, key: str, database_name: str, container_name: str):
        self.endpoint = endpoint
        self.key = key
        self.database_name = database_name
        self.container_name = container_name


def load_config() -> DatabaseConfig:
    endpoint = os.getenv("COSMOS_DB_ENDPOINT", DEFAULT_ENDPOINT)
    key = os.getenv("COSMOS_DB_KEY", DEFAULT_KEY)
    database_name = os.getenv("COSMOS_DB_DATABASE", DEFAULT_DATABASE)
    container_name = os.getenv("COSMOS_DB_CONTAINER", DEFAULT_CONTAINER)
    return DatabaseConfig(endpoint, key, database_name, container_name)


@lru_cache(maxsize=1)
def get_client() -> CosmosClient:
    config = load_config()
    if not config.endpoint or not config.key:
        raise ValueError("COSMOS_DB_ENDPOINT and COSMOS_DB_KEY must be set")
    return CosmosClient(config.endpoint, credential=config.key)


def get_container():
    config = load_config()
    client = get_client()
    database = client.create_database_if_not_exists(id=config.database_name)
    container = database.create_container_if_not_exists(
        id=config.container_name,
        partition_key=PartitionKey(path="/partitionKey"),
        offer_throughput=400,
    )
    return container


def ping() -> bool:
    container = get_container()
    list(container.read_all_items(max_item_count=1))
    return True
