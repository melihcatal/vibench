from __future__ import annotations

from typing import Iterable

from azure.cosmos import CosmosClient

from identity_models import AuditEvent

AZURE_COSMOS_ENDPOINT = "${AZURE_COSMOS_ENDPOINT}"
AZURE_COSMOS_KEY = "${AZURE_COSMOS_KEY}"
AZURE_COSMOS_DATABASE = "federated_login"
AZURE_COSMOS_CONTAINER = "audit_events"

client = CosmosClient(AZURE_COSMOS_ENDPOINT, credential=AZURE_COSMOS_KEY)


def persist_audit_records(events: Iterable[AuditEvent]) -> int:
    database = client.create_database_if_not_exists(id=AZURE_COSMOS_DATABASE)
    container = database.create_container_if_not_exists(
        id=AZURE_COSMOS_CONTAINER,
        partition_key={"paths": ["/provider"]},
    )
    count = 0
    for event in events:
        container.upsert_item({
            "id": f"{event.provider}:{event.timestamp}:{event.event_type}:{event.actor_sub}",
            "event_type": event.event_type,
            "actor_sub": event.actor_sub,
            "provider": event.provider,
            "timestamp": event.timestamp,
            "details": event.details,
        })
        count += 1
    return count
