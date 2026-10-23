from typing import Any, Dict, Optional

from azure.cosmos import exceptions

from database_client import ensure_document_shape, get_container
from database_models import DocumentOperationResponse, DocumentUpsertRequest, normalize_document


def upsert_document(document: Dict[str, Any], partition_key: Optional[str] = None) -> DocumentOperationResponse:
    request = DocumentUpsertRequest(document=document, partition_key=partition_key)
    container = get_container()
    item = ensure_document_shape(normalize_document(request.document), request.partition_key)
    stored = container.upsert_item(item)
    return DocumentOperationResponse(ok=True, document=dict(stored), modified_count=1, message="upserted")


if __name__ == "__main__":
    raise SystemExit("This module exposes upsert_document() for Cosmos DB integration.")
