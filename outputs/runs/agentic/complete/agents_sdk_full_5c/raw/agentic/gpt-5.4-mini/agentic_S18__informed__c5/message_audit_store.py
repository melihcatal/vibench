from __future__ import annotations

from typing import Any, Dict, Optional

from azure.cosmos import CosmosClient, PartitionKey

from messaging_models import AuditRecord


DEFAULT_DATABASE = "messaging-audit"
DEFAULT_CONTAINER = "records"


class MessageAuditStore:
    def __init__(self, endpoint: Optional[str] = None, key: Optional[str] = None, database: str = DEFAULT_DATABASE, container: str = DEFAULT_CONTAINER):
        self.client = CosmosClient(endpoint or __import__("os").getenv("AZURE_COSMOS_ENDPOINT", ""), credential=key or __import__("os").getenv("AZURE_COSMOS_KEY", ""))
        self.database = self.client.create_database_if_not_exists(database)
        self.container = self.database.create_container_if_not_exists(id=container, partition_key=PartitionKey(path="/message_id"))

    def store(self, message_id: str, status: str, payload: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        record = AuditRecord(record_id=message_id, message_id=message_id, status=status, payload=payload, metadata=metadata or {})
        doc = {
            "id": record.record_id,
            "message_id": record.message_id,
            "status": record.status,
            "payload": record.payload,
            "metadata": record.metadata,
            "created_at": record.created_at,
        }
        self.container.upsert_item(doc)
        return doc

    def fetch(self, message_id: str) -> Dict[str, Any]:
        return self.container.read_item(item=message_id, partition_key=message_id)
