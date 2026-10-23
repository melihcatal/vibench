import os
from typing import Dict, Any
from azure.cosmos import CosmosClient, PartitionKey
from database_client import get_cosmos_container
from database_models import normalize_document

def upsert_document(document_id: str, document: Dict[str, Any], partition_key: str) -> Dict[str, Any]:
    """
    Upserts a JSON document into Azure Cosmos DB by its primary identifier.
    """
    container = get_cosmos_container()
    normalized_doc = normalize_document(document)
    normalized_doc['id'] = document_id
    normalized_doc['partitionKey'] = partition_key
    
    response = container.upsert_item(body=normalized_doc)
    return response