from __future__ import annotations

from typing import Any, Dict

from azure.cosmos import CosmosClient

COSMOS_DB_NAME = "expenses"
COSMOS_CONTAINER_NAME = "records"


def expense_record_store(record: Dict[str, Any]) -> Dict[str, Any]:
    client = CosmosClient.from_connection_string(__import__("os").getenv("AZURE_COSMOS_CONNECTION_STRING", ""))
    db = client.create_database_if_not_exists(COSMOS_DB_NAME)
    container = db.create_container_if_not_exists(id=COSMOS_CONTAINER_NAME, partition_key={"paths": ["/vendor"]})
    result = container.upsert_item(record)
    return {"stored": True, "id": result.get("id") if isinstance(result, dict) else record.get("id"), "provider": "azure-cosmos"}
