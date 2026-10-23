from __future__ import annotations

from typing import Any, Dict, Optional

from azure.cosmos.exceptions import CosmosHttpResponseError

from database_client import create_container_if_missing, resolve_partition_key
from database_models import (
    DocumentWriteRequest,
    ensure_document_identity,
    normalize_document,
)


def upsert_document(
    document_id: str, body: Dict[str, Any], partition_key: Optional[str] = None
) -> Dict[str, Any]:
    request = DocumentWriteRequest(
        document_id=document_id, body=body, partition_key=partition_key
    )
    document = ensure_document_identity(request.document_id, request.body)
    pk_value = resolve_partition_key(document, request.partition_key)
    container = create_container_if_missing()
    try:
        response = container.upsert_item(body=document, partition_key=pk_value)
    except CosmosHttpResponseError as exc:
        raise RuntimeError(f"Azure Cosmos DB upsert failed: {exc.message}") from exc
    return normalize_document(response)
