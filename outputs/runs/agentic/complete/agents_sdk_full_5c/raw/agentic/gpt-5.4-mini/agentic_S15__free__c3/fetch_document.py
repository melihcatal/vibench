from __future__ import annotations

from database_client import get_table, get_table_name
from database_models import DocumentFetchRequest, OperationResponse


def fetch_document(document_id: str, table_name: str | None = None) -> OperationResponse:
    request = DocumentFetchRequest(document_id=document_id, table_name=table_name)
    table = get_table(request.table_name)
    result = table.get_item(Key={"document_id": request.document_id})
    item = result.get("Item")
    return OperationResponse(ok=item is not None, data={"table_name": get_table_name(request.table_name), "item": item or {}})
