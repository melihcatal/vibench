from typing import Any, Dict, List
from database_client import DatabaseClient


def query_documents(
    field_name: str, field_value: Any, partition_key: str
) -> List[Dict[str, Any]]:
    client = DatabaseClient().get_container()
    query = f"SELECT * FROM c WHERE c.{field_name} = @value AND c.partition_key = @partition_key"
    parameters = [
        {"name": "@value", "value": field_value},
        {"name": "@partition_key", "value": partition_key},
    ]

    items = list(
        client.query_items(
            query=query, parameters=parameters, enable_cross_partition_query=False
        )
    )

    return [
        {
            "id": item["id"],
            "partition_key": item["partition_key"],
            "document": item,
            "etag": item["_etag"],
        }
        for item in items
    ]
