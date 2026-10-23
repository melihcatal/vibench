from typing import Any, Dict, Optional

from azure.cosmos import exceptions

from database_client import get_container, ensure_document_shape
from database_models import ConditionalUpdateRequest, DocumentOperationResponse, normalize_document


def conditional_update(document_id: str, updates: Dict[str, Any], expected_version: Optional[int] = None, partition_key: Optional[str] = None) -> DocumentOperationResponse:
    request = ConditionalUpdateRequest(document_id=document_id, updates=updates, expected_version=expected_version, partition_key=partition_key)
    container = get_container()
    item = container.read_item(item=request.document_id, partition_key=request.partition_key or request.document_id)
    current_version = item.get("version", 0)
    if request.expected_version is not None and current_version != request.expected_version:
        return DocumentOperationResponse(ok=False, document=normalize_document(item), matched_count=1, message="version-mismatch")
    item.update(request.updates)
    item["version"] = current_version + 1
    stored = container.replace_item(item=request.document_id, body=ensure_document_shape(item, request.partition_key or item.get("partition_key")))
    return DocumentOperationResponse(ok=True, document=dict(stored), modified_count=1, message="conditionally-updated")


if __name__ == "__main__":
    raise SystemExit("This module exposes conditional_update() for version-aware Cosmos DB updates.")
