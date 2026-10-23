import os
from typing import Any, Dict

from azure.cosmos import CosmosClient, PartitionKey

from database_client import get_database_endpoint, get_database_key, get_database_name, get_container_name
from database_models import normalize_document


def get_container():
    client = CosmosClient(get_database_endpoint(), credential=get_database_key())
    database = client.create_database_if_not_exists(id=get_database_name())
    return database.create_container_if_not_exists(id=get_container_name(), partition_key=PartitionKey(path="/id"))


def upsert_document(document: Dict[str, Any]) -> Dict[str, Any]:
    container = get_container()
    normalized = normalize_document(document)
    return container.upsert_item(normalized)


if __name__ == "__main__":
    payload = {"id": os.getenv("DOCUMENT_ID", "doc-1"), "title": os.getenv("DOCUMENT_TITLE", "example")}
    upsert_document(payload)
