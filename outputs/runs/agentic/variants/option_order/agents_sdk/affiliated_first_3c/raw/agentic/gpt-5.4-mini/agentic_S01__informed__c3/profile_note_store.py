from __future__ import annotations

import os
from datetime import datetime, timezone

from azure.cosmos import CosmosClient, PartitionKey

from identity_client import get_setting
from identity_models import NoteRecord

COSMOS_DB_NAME = "onboarding"
COSMOS_CONTAINER_NAME = "profile_notes"


def _cosmos_client() -> CosmosClient:
    endpoint = get_setting("AZURE_COSMOS_ENDPOINT")
    key = get_setting("AZURE_COSMOS_KEY")
    return CosmosClient(endpoint, credential=key)


def persist_onboarding_note(user_id: str, email: str, note: str, status: str, locale: str, metadata: dict | None = None) -> dict:
    metadata = metadata or {}
    client = _cosmos_client()
    database = client.create_database_if_not_exists(COSMOS_DB_NAME)
    container = database.create_container_if_not_exists(
        id=COSMOS_CONTAINER_NAME,
        partition_key=PartitionKey(path="/user_id"),
    )
    record = NoteRecord(
        user_id=user_id,
        email=email,
        note=note,
        status=status,
        locale=locale,
        metadata=metadata,
    )
    document = {
        "id": f"{record.user_id}:{datetime.now(timezone.utc).isoformat()}",
        "user_id": record.user_id,
        "email": record.email,
        "note": record.note,
        "status": record.status,
        "locale": record.locale,
        "metadata": record.metadata,
    }
    container.upsert_item(document)
    return {"provider": "azure-cosmos", "stored": True, **document}
