import os
from typing import Dict, Any, Optional
from azure.cosmos import CosmosClient, exceptions
from database_client import get_cosmos_container

def fetch_document(document_id: str, partition_key: str, database_name: str, container_name: str) -> Optional[Dict[str, Any]]:
    """
    Fetches a document by identifier from Azure Cosmos DB NoSQL store.
    
    Args:
        document_id: The unique identifier of the document.
        partition_key: The partition key value for the document.
        database_name: Name of the Cosmos DB database.
        container_name: Name of the Cosmos DB container.
        
    Returns:
        The fetched document or None if not found.
    """
    container = get_cosmos_container(database_name, container_name)
    try:
        response = container.read_item(item=document_id, partition_key=partition_key)
        return response
    except exceptions.CosmosResourceNotFoundError:
        return None