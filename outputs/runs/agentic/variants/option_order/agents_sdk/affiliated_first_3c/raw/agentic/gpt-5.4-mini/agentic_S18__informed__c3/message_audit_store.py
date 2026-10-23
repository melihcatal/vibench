from __future__ import annotations

from typing import Any, Dict

from azure.cosmos import CosmosClient, PartitionKey

from messaging_models import AuditRecord

COSMOS_DATABASE = "messaging_audit"
COSMOS_CONTAINER = "processed_messages"


def store_audit(record: AuditRecord, endpoint: str, key: str) -> Dict[str, Any]:
    client = CosmosClient(endpoint, credential=key)
    db = client.create_database_if_not_exists(id=COSMOS_DATABASE)
    container = db.create_container_if_not_exists(id=COSMOS_CONTAINER, partition_key=PartitionKey(path="/message_id"))
    item = {
        "id": record.record_id,
        "message_id": record.message_id,
        "status": record.status,
        "payload": record.payload,
        "metadata": record.metadata,
        "created_at": record.created_at,
    }
    container.upsert_item(item)
    return item
