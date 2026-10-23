import os
from typing import Dict, Any
from azure.cosmos import CosmosClient, PartitionKey
from database_client import get_cosmos_container

def upsert_document(document: Dict[str, Any], database_name: str, container_name: str) -> Dict[str, Any]:
    """
    Upserts a JSON document into Azure Cosmos DB NoSQL store by its primary identifier.
    Uses the 'id' field as the primary key.
    """
    container = get_cosmos_container(database_name, container_name)
    response = container.upsert_item(body=document)
    return response