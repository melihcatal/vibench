import os
from typing import Any, Dict, List
from database_client import DatabaseClient


def query_documents(
    field_name: str, field_value: Any, partition_key: str = None
) -> List[Dict[str, Any]]:
    """Queries documents in Azure Cosmos DB by a field value or partition key."""
    client = DatabaseClient()
    container = client.get_container()

    query = f"SELECT * FROM c WHERE c.{field_name} = @value"
    parameters = [{"name": "@value", "value": field_value}]

    if partition_key:
        query += " AND c.partition_key = @partition_key"
        parameters.append({"name": "@partition_key", "value": partition_key})

    try:
        items = list(
            container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=not partition_key,
            )
        )
        return [{"id": item["id"], "body": item} for item in items]
    except Exception as e:
        raise Exception(f"Failed to query documents: {str(e)}")
