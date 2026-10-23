import os
from typing import Dict, Any, Optional
from azure.cosmos import CosmosClient, exceptions
from database_client import get_cosmos_container

def conditional_update(document_id: str, partition_key: str, update_data: Dict[str, Any], etag: Optional[str] = None) -> Dict[str, Any]:
    """
    Applies a conditional or version-aware update to a document in Azure Cosmos DB.
    """
    container = get_cosmos_container()
    try:
        current_doc = container.read_item(item=document_id, partition_key=partition_key)
        if etag and current_doc.get('_etag') != etag:
            raise exceptions.CosmosAccessConditionFailedError("ETag mismatch")
        
        current_doc.update(update_data)
        response = container.replace_item(item=document_id, body=current_doc)
        return response
    except exceptions.CosmosResourceNotFoundError:
        raise ValueError("Document not found")