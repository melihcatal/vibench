from __future__ import annotations

from typing import Any, Dict

from boto3.dynamodb.conditions import Attr

from database_client import get_table, get_table_name
from database_models import DocumentUpsertRequest, OperationResponse, normalize_document


def upsert_document(document_id: str, document: Dict[str, Any], table_name: str | None = None) -> OperationResponse:
    request = DocumentUpsertRequest(document_id=document_id, document=normalize_document(document), table_name=table_name)
    table = get_table(request.table_name)
    payload = {"document_id": request.document_id, **request.document}
    payload["version"] = int(payload.get("version", 0)) + 1
    table.put_item(Item=payload)
    return OperationResponse(ok=True, data={"table_name": get_table_name(request.table_name), "item": payload})
