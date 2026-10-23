import os
from typing import Dict, Any, Optional
from azure.cosmos import CosmosClient, exceptions
from database_client import get_cosmos_container

def conditional_update(document_id: str, partition_key: str, update_func: callable, etag: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Applies a conditional or version-aware update to a document in Azure Cosmos DB.
    """
    container = get_cosmos_container()
    try:
        document = container.read_item(item=document_id, partition_key=partition_key)
        if etag and document['_etag'] != etag:
            raise exceptions.CosmosAccessConditionFailedError("ETag mismatch")
        
        updated_doc = update_func(document)
        response = container.replace_item(item=document_id, body=updated_doc)
        return response
    except exceptions.CosmosResourceNotFoundError:
        return None