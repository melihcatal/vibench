from __future__ import annotations

import os
from typing import Any, Dict

from azure.cosmos import CosmosClient, PartitionKey

from identity_models import AuditEvent, StoredAuditRecord, utc_now_iso



def persist_login_audit_record(event: AuditEvent) -> StoredAuditRecord:
    endpoint = os.environ["AZURE_COSMOSDB_ENDPOINT"]
    key = os.environ["AZURE_COSMOSDB_KEY"]
    database_name = os.environ["AZURE_COSMOSDB_DATABASE"]
    container_name = os.environ["AZURE_COSMOSDB_CONTAINER"]

    client = CosmosClient(endpoint, credential=key)
    database = client.create_database_if_not_exists(id=database_name)
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/provider"),
    )

    document: Dict[str, Any] = {
        "id": event.event_id,
        "provider": event.provider,
        "event_type": event.event_type,
        "actor_subject": event.actor_subject,
        "status": event.status,
        "occurred_at": event.occurred_at,
        "details": event.details,
        "stored_at": utc_now_iso(),
    }
    created = container.upsert_item(document)
    return StoredAuditRecord(
        provider="azure_cosmos_db",
        document_id=created["id"],
        partition_key=created["provider"],
        stored_at=created["stored_at"],
    )
