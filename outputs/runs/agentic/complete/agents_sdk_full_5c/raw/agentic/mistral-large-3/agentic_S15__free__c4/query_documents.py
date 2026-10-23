from typing import Dict, Any, List, Optional
from azure.cosmos import CosmosClient, PartitionKey
from database_client import get_cosmos_container

def query_documents(field_name: str, field_value: Any, partition_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Queries documents by a field value or partition-style key in Azure Cosmos DB NoSQL store.
    """
    container = get_cosmos_container()
    query = f"SELECT * FROM c WHERE c.{field_name} = @value"
    parameters = [{"name": "@value", "value": field_value}]
    
    if partition_key:
        results = list(container.query_items(
            query=query,
            parameters=parameters,
            partition_key=partition_key
        ))
    else:
        results = list(container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
    
    return results