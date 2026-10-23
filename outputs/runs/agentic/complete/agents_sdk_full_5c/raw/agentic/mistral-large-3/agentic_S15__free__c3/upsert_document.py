import os
from typing import Dict, Any
from azure.cosmos import CosmosClient, PartitionKey
from database_client import get_cosmos_container

def upsert_document(document: Dict[str, Any], database_name: str, container_name: str) -> Dict[str, Any]:
    """
    Upserts a JSON document into Azure Cosmos DB NoSQL store by its primary identifier.
    
    Args:
        document: The document to upsert, must include 'id' field.
        database_name: Name of the Cosmos DB database.
        container_name: Name of the Cosmos DB container.
        
    Returns:
        The upserted document as returned by Cosmos DB.
    """
    container = get_cosmos_container(database_name, container_name)
    response = container.upsert_item(body=document)
    return response