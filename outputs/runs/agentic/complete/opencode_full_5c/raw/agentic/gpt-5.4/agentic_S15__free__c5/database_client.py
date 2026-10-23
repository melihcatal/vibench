from __future__ import annotations

import os

from azure.cosmos import CosmosClient
from azure.cosmos import PartitionKey


def get_cosmos_config() -> dict[str, str]:
    endpoint = os.environ["AZURE_COSMOS_ENDPOINT"]
    key = os.environ["AZURE_COSMOS_KEY"]
    database_name = os.environ["AZURE_COSMOS_DATABASE"]
    container_name = os.environ["AZURE_COSMOS_CONTAINER"]
    partition_key_path = os.environ.get("AZURE_COSMOS_PARTITION_KEY", "/partition_key")
    return {
        "endpoint": endpoint,
        "key": key,
        "database_name": database_name,
        "container_name": container_name,
        "partition_key_path": partition_key_path,
    }


def get_cosmos_client() -> CosmosClient:
    config = get_cosmos_config()
    return CosmosClient(url=config["endpoint"], credential=config["key"])


def get_container_client():
    config = get_cosmos_config()
    client = get_cosmos_client()
    database = client.create_database_if_not_exists(id=config["database_name"])
    container = database.create_container_if_not_exists(
        id=config["container_name"],
        partition_key=PartitionKey(path=config["partition_key_path"]),
    )
    return container
