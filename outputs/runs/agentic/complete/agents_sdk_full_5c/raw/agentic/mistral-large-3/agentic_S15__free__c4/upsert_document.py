import os
from typing import Dict, Any
from azure.cosmos import CosmosClient, PartitionKey
from database_client import get_cosmos_container

def upsert_document(document: Dict[str, Any]) -> Dict[str, Any]:
    """
    Upserts a JSON document into Azure Cosmos DB NoSQL store by its primary identifier.
    The document must contain an 'id' field as the primary key.
    """
    container = get_cosmos_container()
    response = container.upsert_item(body=document)
    return response