import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from azure.cosmos import CosmosClient, PartitionKey


@dataclass(frozen=True)
class DatabaseConfig:
    endpoint: str
    key: str
    database_name: str
    container_name: str
    partition_key_path: str = "/id"


def load_config() -> DatabaseConfig:
    return DatabaseConfig(
        endpoint=os.environ["AZURE_COSMOS_ENDPOINT"],
        key=os.environ["AZURE_COSMOS_KEY"],
        database_name=os.environ.get("AZURE_COSMOS_DATABASE", "documents"),
        container_name=os.environ.get("AZURE_COSMOS_CONTAINER", "records"),
        partition_key_path=os.environ.get("AZURE_COSMOS_PARTITION_KEY", "/id"),
    )


@lru_cache(maxsize=1)
def get_client() -> CosmosClient:
    cfg = load_config()
    return CosmosClient(cfg.endpoint, credential=cfg.key)


def get_container():
    cfg = load_config()
    client = get_client()
    database = client.create_database_if_not_exists(cfg.database_name)
    container = database.create_container_if_not_exists(
        id=cfg.container_name,
        partition_key=PartitionKey(path=cfg.partition_key_path),
    )
    return container
