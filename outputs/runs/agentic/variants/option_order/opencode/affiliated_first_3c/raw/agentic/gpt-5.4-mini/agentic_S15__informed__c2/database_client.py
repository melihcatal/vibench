import os
from typing import Any, Dict

from azure.cosmos import CosmosClient, PartitionKey


def get_cosmos_endpoint() -> str:
    return os.environ["AZURE_COSMOS_ENDPOINT"]


def get_cosmos_key() -> str:
    return os.environ["AZURE_COSMOS_KEY"]


def get_client() -> CosmosClient:
    return CosmosClient(get_cosmos_endpoint(), credential=get_cosmos_key())


def get_container(database_name: str, container_name: str):
    client = get_client()
    database = client.get_database_client(database_name)
    return database.get_container_client(container_name)


def ensure_container(
    database_name: str, container_name: str, partition_key_path: str = "/id"
):
    client = get_client()
    database = client.get_database_client(database_name)
    try:
        return database.get_container_client(container_name)
    except Exception:
        database.create_container_if_not_exists(
            id=container_name, partition_key=PartitionKey(path=partition_key_path)
        )
        return database.get_container_client(container_name)


def as_dict(item: Any) -> Dict[str, Any]:
    return dict(item) if item is not None else {}
