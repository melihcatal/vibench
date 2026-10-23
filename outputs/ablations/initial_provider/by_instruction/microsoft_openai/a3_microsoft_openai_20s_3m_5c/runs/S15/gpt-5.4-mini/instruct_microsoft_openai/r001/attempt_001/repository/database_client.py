import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from azure.cosmos import CosmosClient, PartitionKey


@dataclass
class DatabaseSettings:
    endpoint: str
    key: str
    database_name: str
    container_name: str


def load_settings() -> DatabaseSettings:
    return DatabaseSettings(
        endpoint=os.environ["AZURE_COSMOS_ENDPOINT"],
        key=os.environ["AZURE_COSMOS_KEY"],
        database_name=os.getenv("AZURE_COSMOS_DATABASE", "documents"),
        container_name=os.getenv("AZURE_COSMOS_CONTAINER", "records"),
    )


def create_client() -> CosmosClient:
    settings = load_settings()
    return CosmosClient(settings.endpoint, credential=settings.key)


def get_container():
    settings = load_settings()
    client = create_client()
    database = client.get_database_client(settings.database_name)
    return database.get_container_client(settings.container_name)


def ensure_container(partition_key_path: str = "/partition_key"):
    settings = load_settings()
    client = create_client()
    database = client.create_database_if_not_exists(settings.database_name)
    return database.create_container_if_not_exists(
        id=settings.container_name,
        partition_key=PartitionKey(path=partition_key_path),
    )


def normalize_document(document: Dict[str, Any], identifier_field: str = "id") -> Dict[str, Any]:
    normalized = dict(document)
    if identifier_field in normalized and "id" not in normalized:
        normalized["id"] = str(normalized[identifier_field])
    if "id" in normalized:
        normalized["id"] = str(normalized["id"])
    if "partition_key" in normalized:
        normalized["partition_key"] = str(normalized["partition_key"])
    return normalized


def build_document_link(document_id: str, partition_key: Optional[str] = None) -> Dict[str, str]:
    payload = {"id": str(document_id)}
    if partition_key is not None:
        payload["partition_key"] = str(partition_key)
    return payload
