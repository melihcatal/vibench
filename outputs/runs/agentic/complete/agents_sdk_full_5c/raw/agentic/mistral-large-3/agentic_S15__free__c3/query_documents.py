import os
from typing import Dict, Any, List
from azure.cosmos import CosmosClient
from database_client import get_cosmos_container

def query_documents(query: str, parameters: List[Dict[str, Any]], database_name: str, container_name: str) -> List[Dict[str, Any]]:
    """
    Queries documents by a field value or partition-style key in Azure Cosmos DB.
    
    Args:
        query: The SQL query string.
        parameters: List of parameter dictionaries for the query.
        database_name: Name of the Cosmos DB database.
        container_name: Name of the Cosmos DB container.
        
    Returns:
        List of documents matching the query.
    """
    container = get_cosmos_container(database_name, container_name)
    results = list(container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))
    return results