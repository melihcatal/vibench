import os
from typing import Any, Dict, Optional

from azure.cosmos import CosmosClient, PartitionKey

from database_models import normalize_document


def get_config() -> Dict[str, str]:
    return {
        "endpoint": os.getenv("AZURE_COSMOS_ENDPOINT", ""),
        "key": os.getenv("AZURE_COSMOS_KEY", ""),
        "database": os.getenv("AZURE_COSMOS_DATABASE", "documents"),
        "container": os.getenv("AZURE_COSMOS_CONTAINER", "records"),
        "partition_key": os.getenv("AZURE_COSMOS_PARTITION_KEY", "/id"),
    }


def get_client() -> CosmosClient:
    config = get_config()
    return CosmosClient(config["endpoint"], credential=config["key"])


def get_container():
    config = get_config()
    client = get_client()
    database = client.get_database_client(config["database"])
    return database.get_container_client(config["container"])


def upsert_item(document: Dict[str, Any], primary_key: str = "id") -> Dict[str, Any]:
    container = get_container()
    normalized = normalize_document(document, primary_key=primary_key)
    return container.upsert_item(normalized)


def read_item(document_id: str, partition_value: Optional[str] = None) -> Dict[str, Any]:
    container = get_container()
    if partition_value is None:
        partition_value = document_id
    return container.read_item(item=document_id, partition_key=partition_value)


def query_items(query: str, parameters: Optional[list] = None):
    container = get_container()
    return list(container.query_items(query=query, parameters=parameters or [], enable_cross_partition_query=True))


def replace_item(document_id: str, body: Dict[str, Any], partition_value: Optional[str] = None) -> Dict[str, Any]:
    container = get_container()
    if partition_value is None:
        partition_value = document_id
    return container.replace_item(item=document_id, body=body, partition_key=partition_value)
