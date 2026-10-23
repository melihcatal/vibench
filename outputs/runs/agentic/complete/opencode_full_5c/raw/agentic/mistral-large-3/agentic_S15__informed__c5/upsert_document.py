from azure.cosmos import CosmosClient, exceptions
import os
import json
from typing import Dict, Any


def upsert_document(
    database_name: str,
    container_name: str,
    document_id: str,
    document: Dict[str, Any],
    partition_key: str = None,
) -> Dict[str, Any]:
    """
    Upserts a JSON document into Azure Cosmos DB for NoSQL.

    Args:
        database_name: Name of the database
        container_name: Name of the container
        document_id: Primary identifier of the document
        document: JSON document to upsert
        partition_key: Optional partition key value

    Returns:
        The upserted document
    """
    endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
    key = os.getenv("AZURE_COSMOS_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_COSMOS_ENDPOINT and AZURE_COSMOS_KEY must be set")

    client = CosmosClient(endpoint, key)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)

    document["id"] = document_id
    if partition_key:
        document["partitionKey"] = partition_key

    try:
        response = container.upsert_item(document)
        return response
    except exceptions.CosmosHttpResponseError as e:
        raise Exception(f"Failed to upsert document: {e.message}")
