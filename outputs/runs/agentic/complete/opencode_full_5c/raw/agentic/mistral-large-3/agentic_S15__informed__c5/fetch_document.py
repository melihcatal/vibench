from azure.cosmos import CosmosClient, exceptions
import os
from typing import Dict, Any, Optional


def fetch_document(
    database_name: str,
    container_name: str,
    document_id: str,
    partition_key: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Fetches a document by its identifier from Azure Cosmos DB for NoSQL.

    Args:
        database_name: Name of the database
        container_name: Name of the container
        document_id: Primary identifier of the document
        partition_key: Optional partition key value

    Returns:
        The fetched document or None if not found
    """
    endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
    key = os.getenv("AZURE_COSMOS_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_COSMOS_ENDPOINT and AZURE_COSMOS_KEY must be set")

    client = CosmosClient(endpoint, key)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)

    try:
        response = container.read_item(item=document_id, partition_key=partition_key)
        return response
    except exceptions.CosmosResourceNotFoundError:
        return None
    except exceptions.CosmosHttpResponseError as e:
        raise Exception(f"Failed to fetch document: {e.message}")
