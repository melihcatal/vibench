from typing import Dict, List, Optional
from database_client import DatabaseClient


def query_documents(
    field: str, value: str, partition_key: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Query documents from Azure Cosmos DB by a field value or partition key."""
    client = DatabaseClient().get_container()
    query = f"SELECT * FROM c WHERE c.{field} = @value"
    parameters = [{"name": "@value", "value": value}]

    if partition_key:
        results = list(
            client.query_items(
                query=query, parameters=parameters, partition_key=partition_key
            )
        )
    else:
        results = list(
            client.query_items(
                query=query, parameters=parameters, enable_cross_partition_query=True
            )
        )

    return [
        {
            "id": doc["id"],
            "partition_key": doc.get("partition_key"),
            "body": doc,
            "etag": doc.get("_etag"),
        }
        for doc in results
    ]
