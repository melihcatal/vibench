from __future__ import annotations

from database_client import get_table, service_error_payload
from database_models import DocumentKey, FetchRequest, OperationResponse


def fetch_document(request: FetchRequest) -> OperationResponse:
    try:
        table = get_table(request.table_name)
        key = {"document_id": request.key.document_id}
        if request.key.partition_key is not None:
            key["partition_key"] = request.key.partition_key
        response = table.get_item(Key=key)
        item = response.get("Item")
        if not item:
            return OperationResponse(ok=False, error={"error_type": "NotFound", "message": "Document not found"})
        return OperationResponse(ok=True, data={"document": item})
    except Exception as exc:
        return OperationResponse(ok=False, error=service_error_payload(exc))
