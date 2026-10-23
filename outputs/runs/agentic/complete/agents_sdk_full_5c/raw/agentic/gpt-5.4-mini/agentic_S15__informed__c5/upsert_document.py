from __future__ import annotations

from typing import Any, Dict

from azure.cosmos.exceptions import CosmosHttpResponseError

from database_client import build_document_id, get_container_client, partition_key_from_payload
from database_models import NormalizedResponse, normalize_document


def upsert_document(document: Dict[str, Any], database_name: str = "documents", container_name: str = "records") -> NormalizedResponse:
    container = get_container_client(database_name, container_name)
    normalized = normalize_document(document)
    normalized["id"] = build_document_id(normalized)
    partition_key = partition_key_from_payload(normalized)
    try:
        if partition_key is None:
            result = container.upsert_item(normalized)
        else:
            result = container.upsert_item(normalized, partition_key=partition_key)
        return NormalizedResponse(ok=True, data=result, etag=getattr(result, "_etag", None), request_charge=getattr(result, "_request_charge", None))
    except CosmosHttpResponseError as exc:
        return NormalizedResponse(ok=False, data={"error": str(exc), "status_code": getattr(exc, "status_code", None)})
