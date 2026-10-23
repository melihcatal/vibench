from typing import Dict, Any, Optional
from azure.cosmos import CosmosClient, exceptions
from database_client import get_cosmos_container

def conditional_update(
    document_id: str,
    partition_key: str,
    update_expression: Dict[str, Any],
    etag: Optional[str] = None,
    database_name: str = "default_db",
    container_name: str = "default_container"
) -> Optional[Dict[str, Any]]:
    """
    Applies a conditional or version-aware update to a document in Azure Cosmos DB NoSQL store.
    Uses the document's ETag for optimistic concurrency control.
    """
    container = get_cosmos_container(database_name, container_name)
    try:
        document = container.read_item(item=document_id, partition_key=partition_key)
        if etag and document["_etag"] != etag:
            raise exceptions.CosmosAccessConditionFailedError("ETag mismatch")

        document.update(update_expression)
        response = container.replace_item(item=document_id, body=document)
        return response
    except exceptions.CosmosResourceNotFoundError:
        return None