import os
from functools import lru_cache

from azure.cosmos import CosmosClient


def get_database_config():
    return {
        "endpoint": os.getenv("AZURE_COSMOS_ENDPOINT", ""),
        "key": os.getenv("AZURE_COSMOS_KEY", ""),
        "database_name": os.getenv("AZURE_COSMOS_DATABASE", "documents"),
        "container_name": os.getenv("AZURE_COSMOS_CONTAINER", "records"),
    }


@lru_cache(maxsize=1)
def get_cosmos_client():
    cfg = get_database_config()
    if not cfg["endpoint"] or not cfg["key"]:
        raise ValueError("AZURE_COSMOS_ENDPOINT and AZURE_COSMOS_KEY are required")
    return CosmosClient(cfg["endpoint"], credential=cfg["key"])


def get_container():
    cfg = get_database_config()
    client = get_cosmos_client()
    database = client.get_database_client(cfg["database_name"])
    return database.get_container_client(cfg["container_name"])
