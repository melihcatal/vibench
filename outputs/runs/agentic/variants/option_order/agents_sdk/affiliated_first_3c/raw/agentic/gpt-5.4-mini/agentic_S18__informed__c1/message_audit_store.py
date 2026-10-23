from __future__ import annotations

from typing import Any, Dict

from azure.cosmos import CosmosClient, PartitionKey

from messaging_models import AuditRecord


CONTAINER_NAME = "message-audit"
DATABASE_NAME = "messaging"


def persist_processed_message_record(endpoint: str, key: str, record: Dict[str, Any]) -> Dict[str, Any]:
    client = CosmosClient(endpoint, credential=key)
    database = client.create_database_if_not_exists(id=DATABASE_NAME)
    container = database.create_container_if_not_exists(id=CONTAINER_NAME, partition_key=PartitionKey(path="/message_id"))
    audit = AuditRecord(message_id=str(record["message_id"]), status=str(record.get("status", "processed")), payload=dict(record))
    item = {"id": audit.message_id, "message_id": audit.message_id, "status": audit.status, "payload": audit.payload, "processed_at": audit.processed_at}
    container.upsert_item(item)
    return item
