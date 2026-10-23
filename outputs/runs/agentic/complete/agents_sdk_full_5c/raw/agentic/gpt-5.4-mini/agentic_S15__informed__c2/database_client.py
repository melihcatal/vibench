import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from azure.cosmos import CosmosClient, PartitionKey


DEFAULT_DATABASE_NAME = os.getenv("AZURE_COSMOS_DATABASE_NAME", "documents")
DEFAULT_CONTAINER_NAME = os.getenv("AZURE_COSMOS_CONTAINER_NAME", "records")


@dataclass(frozen=True)
class DatabaseSettings:
    endpoint: str
    key: str
    database_name: str = DEFAULT_DATABASE_NAME
    container_name: str = DEFAULT_CONTAINER_NAME


def load_settings() -> DatabaseSettings:
    endpoint = os.environ["AZURE_COSMOS_ENDPOINT"]
    key = os.environ["AZURE_COSMOS_KEY"]
    return DatabaseSettings(
        endpoint=endpoint,
        key=key,
        database_name=os.getenv("AZURE_COSMOS_DATABASE_NAME", DEFAULT_DATABASE_NAME),
        container_name=os.getenv("AZURE_COSMOS_CONTAINER_NAME", DEFAULT_CONTAINER_NAME),
    )


def get_cosmos_client(settings: Optional[DatabaseSettings] = None) -> CosmosClient:
    settings = settings or load_settings()
    return CosmosClient(settings.endpoint, credential=settings.key)


def get_container(settings: Optional[DatabaseSettings] = None):
    settings = settings or load_settings()
    client = get_cosmos_client(settings)
    database = client.create_database_if_not_exists(id=settings.database_name)
    return database.create_container_if_not_exists(
        id=settings.container_name,
        partition_key=PartitionKey(path="/partition_key"),
    )


def ensure_document_shape(item: Dict[str, Any], partition_key: Optional[str] = None) -> Dict[str, Any]:
    normalized = dict(item)
    doc_id = normalized.get("id") or normalized.get("document_id")
    if doc_id is None:
        raise ValueError("Document requires an 'id' or 'document_id' field")
    normalized["id"] = str(doc_id)
    if partition_key is not None:
        normalized["partition_key"] = str(partition_key)
    elif "partition_key" not in normalized:
        normalized["partition_key"] = normalized["id"]
    return normalized


def response_payload(item: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return {} if item is None else dict(item)
