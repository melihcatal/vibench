from __future__ import annotations

import os
from typing import Any, Dict, Optional

from azure.cosmos import CosmosClient, PartitionKey


DEFAULT_DATABASE = "expenses"
DEFAULT_CONTAINER = "expense_records"


def expense_record_store(record: Dict[str, Any], record_id: Optional[str] = None) -> Dict[str, Any]:
    client = CosmosClient(
        url=os.environ["AZURE_COSMOS_ENDPOINT"],
        credential=os.environ["AZURE_COSMOS_KEY"],
    )
    database = client.create_database_if_not_exists(id=DEFAULT_DATABASE)
    container = database.create_container_if_not_exists(
        id=DEFAULT_CONTAINER,
        partition_key=PartitionKey(path="/record_type"),
    )
    item = dict(record)
    item["id"] = record_id or item.get("id") or f"expense-{abs(hash(str(record))) }"
    created = container.upsert_item(item)
    return {
        "provider": "Azure Cosmos DB for NoSQL",
        "id": created["id"],
        "record_type": created.get("record_type"),
        "stored": True,
    }
