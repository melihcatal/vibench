from __future__ import annotations

from typing import Any, Dict

from azure.cosmos.exceptions import CosmosHttpResponseError

from database_client import CosmosDocumentStore, resolve_partition_key
from database_models import UpsertRequest, normalize_document



def upsert_document(document: Dict[str, Any], partition_key: str | None = None) -> Dict[str, Any]:
    document_id = str(document.get("id") or document.get("document_id"))
    request = UpsertRequest(
        document_id=document_id,
        payload=document,
        partition_key=resolve_partition_key(partition_key, document_id),
    )
    container = CosmosDocumentStore().get_container()
    try:
        result = container.upsert_item(body=request.to_cosmos_item())
        return normalize_document(result)
    except CosmosHttpResponseError as exc:
        raise RuntimeError(f"Azure Cosmos DB upsert failed: {exc}") from exc
