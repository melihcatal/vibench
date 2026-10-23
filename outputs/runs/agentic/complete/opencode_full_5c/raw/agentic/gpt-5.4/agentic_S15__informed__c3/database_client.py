from __future__ import annotations

import os
from typing import Any
from typing import Dict
from typing import Optional

from azure.cosmos import CosmosClient
from azure.cosmos import PartitionKey


def get_cosmos_config() -> Dict[str, str]:
    endpoint = os.environ["AZURE_COSMOS_ENDPOINT"]
    key = os.environ["AZURE_COSMOS_KEY"]
    database_name = os.environ["AZURE_COSMOS_DATABASE"]
    container_name = os.environ["AZURE_COSMOS_CONTAINER"]
    partition_key_path = os.getenv("AZURE_COSMOS_PARTITION_KEY_PATH", "/partition_key")
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


def get_container_client() -> Any:
    config = get_cosmos_config()
    client = get_cosmos_client()
    database = client.get_database_client(config["database_name"])
    return database.get_container_client(config["container_name"])


def ensure_container() -> Any:
    config = get_cosmos_config()
    client = get_cosmos_client()
    database = client.create_database_if_not_exists(id=config["database_name"])
    return database.create_container_if_not_exists(
        id=config["container_name"],
        partition_key=PartitionKey(path=config["partition_key_path"]),
    )


def resolve_partition_key(
    document: Dict[str, Any], explicit_partition_key: Optional[str] = None
) -> str:
    if explicit_partition_key is not None:
        return str(explicit_partition_key)
    if "partition_key" in document and document["partition_key"] is not None:
        return str(document["partition_key"])
    raise ValueError("partition key is required for Azure Cosmos DB operations")
