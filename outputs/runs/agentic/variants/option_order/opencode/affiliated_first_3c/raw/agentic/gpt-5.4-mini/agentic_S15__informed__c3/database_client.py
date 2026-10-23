import os
from functools import lru_cache

from azure.cosmos import CosmosClient, PartitionKey


def get_env(name, default=None):
    value = os.getenv(name)
    return default if value is None or value == "" else value


def get_cosmos_endpoint():
    return get_env("AZURE_COSMOS_ENDPOINT")


def get_cosmos_key():
    return get_env("AZURE_COSMOS_KEY")


def get_cosmos_database_name():
    return get_env("AZURE_COSMOS_DATABASE", "documents")


def get_cosmos_container_name():
    return get_env("AZURE_COSMOS_CONTAINER", "records")


@lru_cache(maxsize=1)
def get_client():
    endpoint = get_cosmos_endpoint()
    key = get_cosmos_key()
    if not endpoint or not key:
        raise ValueError("AZURE_COSMOS_ENDPOINT and AZURE_COSMOS_KEY are required")
    return CosmosClient(endpoint, credential=key)


@lru_cache(maxsize=1)
def get_container():
    client = get_client()
    database = client.get_database_client(get_cosmos_database_name())
    return database.get_container_client(get_cosmos_container_name())


def ensure_container(partition_key_path="/id"):
    client = get_client()
    database = client.create_database_if_not_exists(get_cosmos_database_name())
    return database.create_container_if_not_exists(
        id=get_cosmos_container_name(),
        partition_key=PartitionKey(path=partition_key_path),
        offer_throughput=400,
    )
