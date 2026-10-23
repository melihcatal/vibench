import os
from typing import Dict, Any, Optional
from azure.cosmos import CosmosClient, exceptions
from database_client import get_cosmos_container

def fetch_document(document_id: str, partition_key: str) -> Optional[Dict[str, Any]]:
    """
    Fetches a document from Azure Cosmos DB by its identifier and partition key.
    """
    container = get_cosmos_container()
    try:
        response = container.read_item(item=document_id, partition_key=partition_key)
        return response
    except exceptions.CosmosResourceNotFoundError:
        return None