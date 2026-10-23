from __future__ import annotations

from typing import Any, Dict

from azure.cosmos import CosmosClient, PartitionKey


def expense_record_store(record: Dict[str, Any]) -> Dict[str, Any]:
    endpoint = __import__("os").getenv("AZURE_COSMOS_ENDPOINT", "")
    key = __import__("os").getenv("AZURE_COSMOS_KEY", "")
    client = CosmosClient(endpoint, credential=key)
    db = client.create_database_if_not_exists(id="expenses")
    container = db.create_container_if_not_exists(
        id="records",
        partition_key=PartitionKey(path="/vendor"),
        offer_throughput=400,
    )
    stored = container.upsert_item(record)
    return {"stored": True, "id": stored.get("id"), "vendor": stored.get("vendor")}
