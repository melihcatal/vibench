from typing import Dict, Any, Optional
from azure.cosmos import CosmosClient, exceptions
from database_client import get_cosmos_container

def conditional_update(document_id: str, update_payload: Dict[str, Any], etag: Optional[str] = None) -> Dict[str, Any]:
    """
    Applies a conditional or version-aware update to a document in Azure Cosmos DB NoSQL store.
    Uses etag for optimistic concurrency control.
    """
    container = get_cosmos_container()
    
    if etag:
        update_payload['_etag'] = etag
    
    try:
        response = container.replace_item(item=document_id, body=update_payload)
        return response
    except exceptions.CosmosAccessConditionFailedError:
        raise ValueError("Conditional update failed due to version conflict.")