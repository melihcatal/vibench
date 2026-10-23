from azure.cosmos import CosmosClient, exceptions
import os
from typing import Dict, Any, Optional


def conditional_update(
    database_name: str,
    container_name: str,
    document_id: str,
    update_document: Dict[str, Any],
    condition: str,
    partition_key: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Applies a conditional or version-aware update to a document in Azure Cosmos DB for NoSQL.

    Args:
        database_name: Name of the database
        container_name: Name of the container
        document_id: Primary identifier of the document
        update_document: Document updates to apply
        condition: SQL condition string for the update
        partition_key: Optional partition key value

    Returns:
        The updated document or None if condition failed
    """
    endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
    key = os.getenv("AZURE_COSMOS_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_COSMOS_ENDPOINT and AZURE_COSMOS_KEY must be set")

    client = CosmosClient(endpoint, key)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)

    try:
        # Fetch the current document to merge updates
        current_doc = container.read_item(item=document_id, partition_key=partition_key)
        updated_doc = {**current_doc, **update_document}
        updated_doc["id"] = document_id

        # Apply conditional update
        response = container.replace_item(
            item=document_id, body=updated_doc, conditions=condition
        )
        return response
    except exceptions.CosmosAccessConditionFailedError:
        return None
    except exceptions.CosmosHttpResponseError as e:
        raise Exception(f"Failed to update document: {e.message}")
