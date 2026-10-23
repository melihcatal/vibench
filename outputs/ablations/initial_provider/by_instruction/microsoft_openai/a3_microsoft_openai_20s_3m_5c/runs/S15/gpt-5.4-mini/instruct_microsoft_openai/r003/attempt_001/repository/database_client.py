import os
from functools import lru_cache

from azure.cosmos import CosmosClient


def _env(name, default=None):
    value = os.getenv(name, default)
    if value is None:
        raise ValueError(name)
    return value


@lru_cache(maxsize=1)
def get_cosmos_client():
    return CosmosClient(_env("AZURE_COSMOS_ENDPOINT"), credential=_env("AZURE_COSMOS_KEY"))


def get_database_name():
    return _env("AZURE_COSMOS_DATABASE", "documents")


def get_container_name():
    return _env("AZURE_COSMOS_CONTAINER", "records")


def get_container():
    client = get_cosmos_client()
    return client.get_database_client(get_database_name()).get_container_client(get_container_name())
