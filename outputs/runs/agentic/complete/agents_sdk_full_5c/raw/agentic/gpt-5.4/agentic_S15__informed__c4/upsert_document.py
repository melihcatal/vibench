from __future__ import annotations

from typing import Any, Dict

from database_client import ensure_container
from database_models import DocumentRecord, OperationResult, normalize_document


def upsert_document(document_id: str, payload: Dict[str, Any], partition_key: str) -> OperationResult:
    container = ensure_container()
    record = DocumentRecord(document_id=document_id, payload=payload, partition_key=partition_key)
    response = container.upsert_item(body=record.to_cosmos_item())
    return OperationResult(
        success=True,
        document=normalize_document(response),
        etag=response.get("_etag"),
        status_message="Upserted document in Azure Cosmos DB",
    )
