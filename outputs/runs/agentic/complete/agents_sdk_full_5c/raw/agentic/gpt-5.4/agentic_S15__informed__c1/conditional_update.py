from __future__ import annotations

from typing import Any, Dict

from azure.cosmos.exceptions import CosmosHttpResponseError
from azure.cosmos.partition_key import NonePartitionKeyValue

from database_client import get_container, get_cosmos_client
from database_models import DocumentRecord, normalize_document, utc_now_iso


def conditional_update(document_id: str, partition_key: str, updates: Dict[str, Any], etag: str) -> DocumentRecord | None:
    client = get_cosmos_client()
    container = get_container(client)

    operations = []
    for key, value in updates.items():
        path = f"/{key}"
        operations.append({"op": "set", "path": path, "value": value})
    operations.append({"op": "set", "path": "/updated_at", "value": utc_now_iso()})

    try:
        updated = container.patch_item(
            item=document_id,
            partition_key=partition_key if partition_key is not None else NonePartitionKeyValue,
            patch_operations=operations,
            etag=etag,
            match_condition="IfNotModified",
        )
    except CosmosHttpResponseError:
        return None

    return DocumentRecord.from_cosmos_item(normalize_document(updated) | {"_etag": updated.get("_etag")})
