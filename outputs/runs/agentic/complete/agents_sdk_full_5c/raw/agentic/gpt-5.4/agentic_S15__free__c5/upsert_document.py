from __future__ import annotations

from typing import Any, Dict

from database_client import get_container
from database_models import DocumentRecord, OperationResult, normalize_document


def upsert_document(document: Dict[str, Any], document_id: str, partition_key: str) -> OperationResult:
    container = get_container()
    record = DocumentRecord(id=document_id, partition_key=partition_key, body=document)
    response = container.upsert_item(body=record.to_cosmos_item())
    return OperationResult(
        ok=True,
        item=normalize_document(response),
        etag=response.get("_etag"),
        status_code=200,
        message="Upserted in Azure Cosmos DB",
    )
