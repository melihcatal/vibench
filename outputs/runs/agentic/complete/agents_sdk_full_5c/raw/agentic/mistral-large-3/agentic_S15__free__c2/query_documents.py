import os
from typing import Dict, Any, List
from azure.cosmos import CosmosClient
from database_client import get_cosmos_container

def query_documents(field_name: str, field_value: str, partition_key: str) -> List[Dict[str, Any]]:
    """
    Queries documents from Azure Cosmos DB NoSQL store by a field value or partition key.
    """
    container = get_cosmos_container()
    query = f"SELECT * FROM c WHERE c.{field_name} = @value AND c.partitionKey = @partition_key"
    parameters = [
        {"name": "@value", "value": field_value},
        {"name": "@partition_key", "value": partition_key}
    ]
    items = list(container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=False
    ))
    return items