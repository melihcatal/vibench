import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from azure.cosmos import CosmosClient, PartitionKey


@dataclass(frozen=True)
class DatabaseSettings:
    endpoint: str
    key: str
    database_name: str
    container_name: str
    partition_key_path: str = "/id"


def load_settings() -> DatabaseSettings:
    return DatabaseSettings(
        endpoint=os.environ["AZURE_COSMOS_ENDPOINT"],
        key=os.environ["AZURE_COSMOS_KEY"],
        database_name=os.getenv("AZURE_COSMOS_DATABASE", "documents"),
        container_name=os.getenv("AZURE_COSMOS_CONTAINER", "records"),
        partition_key_path=os.getenv("AZURE_COSMOS_PARTITION_KEY", "/id"),
    )


def create_client(settings: Optional[DatabaseSettings] = None) -> CosmosClient:
    cfg = settings or load_settings()
    return CosmosClient(cfg.endpoint, credential=cfg.key)


def get_container(client: CosmosClient, settings: Optional[DatabaseSettings] = None):
    cfg = settings or load_settings()
    db = client.create_database_if_not_exists(cfg.database_name)
    db.create_container_if_not_exists(
        id=cfg.container_name,
        partition_key=PartitionKey(path=cfg.partition_key_path),
    )
    return db.get_container_client(cfg.container_name)
