import os
from dataclasses import dataclass

from azure.cosmos import CosmosClient, PartitionKey


@dataclass(frozen=True)
class DatabaseConfig:
    endpoint: str
    key: str
    database_name: str
    container_name: str


def load_config() -> DatabaseConfig:
    return DatabaseConfig(
        endpoint=os.environ["AZURE_COSMOS_ENDPOINT"],
        key=os.environ["AZURE_COSMOS_KEY"],
        database_name=os.getenv("AZURE_COSMOS_DATABASE", "documents"),
        container_name=os.getenv("AZURE_COSMOS_CONTAINER", "records"),
    )


def get_container(config: DatabaseConfig | None = None):
    cfg = config or load_config()
    client = CosmosClient(cfg.endpoint, credential=cfg.key)
    database = client.get_database_client(cfg.database_name)
    try:
        container = database.get_container_client(cfg.container_name)
    except Exception:
        database.create_container_if_not_exists(
            id=cfg.container_name,
            partition_key=PartitionKey(path="/id"),
        )
        container = database.get_container_client(cfg.container_name)
    return container
