import os
from typing import Dict, Any
from azure.cosmos import CosmosClient, PartitionKey
from database_client import get_cosmos_container
from database_models import DocumentRequest

def upsert_document(document_id: str, document_data: Dict[str, Any], partition_key: str) -> Dict[str, Any]:
    """
    Upserts a JSON document into Azure Cosmos DB NoSQL store by its primary identifier.
    """
    container = get_cmos_container()
    document_request = DocumentRequest(
        id=document_id,
        partitionKey=partition_key,
        **document_data
    ).dict()
    response = container.upsert_item(body=document_request)
    return response