from typing import Any, Dict

from azure.cosmos import CosmosClient


def expense_record_store(
    record: Dict[str, Any],
    endpoint: str,
    key: str,
    database_name: str,
    container_name: str,
) -> Dict[str, Any]:
    client = CosmosClient(endpoint, key)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    result = container.upsert_item(record)
    return {"stored": True, "result": result}
