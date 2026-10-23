from __future__ import annotations

from typing import Any

from azure.cosmos.exceptions import CosmosHttpResponseError
from azure.cosmos.partition_key import NonePartitionKeyValue

from database_client import get_container
from database_models import build_document_record, normalize_document


def conditional_update(
    document_id: str,
    updates: dict[str, Any],
    partition_key: str | None = None,
    etag: str | None = None,
) -> dict[str, Any]:
    container = get_container()
    resolved_partition_key = partition_key or document_id
    current = container.read_item(
        item=document_id, partition_key=resolved_partition_key
    )
    merged = dict(current)
    merged.update(updates)
    normalized = normalize_document(
        merged, document_id=document_id, partition_key=resolved_partition_key
    )
    access_condition = (
        {"type": "IfMatch", "condition": etag or current.get("_etag")}
        if (etag or current.get("_etag"))
        else None
    )
    try:
        item = (
            container.replace_item(
                item=document_id,
                body=normalized,
                partition_key=resolved_partition_key
                if resolved_partition_key is not None
                else NonePartitionKeyValue,
                etag=(etag or current.get("_etag")),
                match_condition="IfNotModified",
            )
            if access_condition
            else container.replace_item(
                item=document_id, body=normalized, partition_key=resolved_partition_key
            )
        )
    except CosmosHttpResponseError as exc:
        raise RuntimeError(
            "conditional update failed for Azure Cosmos DB document"
        ) from exc
    record = build_document_record(item)
    return {
        "provider": "azure-cosmos",
        "document_id": record.document_id,
        "partition_key": record.partition_key,
        "etag": record.etag,
        "updated_at": record.updated_at,
        "body": record.body,
    }
