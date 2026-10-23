import os
from typing import Dict, Any, Optional
from azure.cosmos import CosmosClient, exceptions
from database_client import get_cosmos_container

def conditional_update(
    document_id: str, 
    partition_key: str, 
    update_expression: Dict[str, Any], 
    condition_expression: str, 
    database_name: str, 
    container_name: str
) -> Optional[Dict[str, Any]]:
    """
    Applies a conditional or version-aware update to a document in Azure Cosmos DB.
    
    Args:
        document_id: The unique identifier of the document.
        partition_key: The partition key value for the document.
        update_expression: The update to apply to the document.
        condition_expression: The condition that must be met for the update to proceed.
        database_name: Name of the Cosmos DB database.
        container_name: Name of the Cosmos DB container.
        
    Returns:
        The updated document or None if the condition was not met.
    """
    container = get_cosmos_container(database_name, container_name)
    try:
        document = container.read_item(item=document_id, partition_key=partition_key)
        if not eval(condition_expression, {}, document):
            return None
        document.update(update_expression)
        response = container.replace_item(item=document_id, body=document)
        return response
    except exceptions.CosmosResourceNotFoundError:
        return None