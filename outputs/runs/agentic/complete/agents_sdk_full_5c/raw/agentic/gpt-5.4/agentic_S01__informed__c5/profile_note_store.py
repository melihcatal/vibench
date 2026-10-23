from __future__ import annotations

import os
from typing import Any, Mapping, Optional

from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.exceptions import CosmosResourceNotFoundError

from identity_models import DocumentWriteResult


DEFAULT_DATABASE = "onboarding"
DEFAULT_CONTAINER = "profile_notes"


def _get_container():
    endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
    key = os.getenv("AZURE_COSMOS_KEY")
    if not endpoint or not key:
        raise RuntimeError("Missing required environment variables: AZURE_COSMOS_ENDPOINT and/or AZURE_COSMOS_KEY")
    database_name = os.getenv("AZURE_COSMOS_DATABASE", DEFAULT_DATABASE)
    container_name = os.getenv("AZURE_COSMOS_CONTAINER", DEFAULT_CONTAINER)
    client = CosmosClient(endpoint, credential=key)
    database = client.create_database_if_not_exists(id=database_name)
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/user_id"),
    )
    return container


def profile_note_store(user_id: str, note: str, metadata: Optional[Mapping[str, Any]] = None) -> DocumentWriteResult:
    container = _get_container()
    document = {
        "id": f"note:{user_id}",
        "user_id": user_id,
        "note": note,
        "metadata": dict(metadata or {}),
    }
    existing = None
    try:
        existing = container.read_item(item=document["id"], partition_key=user_id)
    except CosmosResourceNotFoundError:
        existing = None
    if existing:
        existing.update(document)
        result = container.replace_item(item=document["id"], body=existing)
    else:
        result = container.create_item(body=document)
    return DocumentWriteResult(document_id=result["id"], etag=result.get("_etag"), provider="azure_cosmos_db")
