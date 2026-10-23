from __future__ import annotations

from typing import Any, Dict

from boto3.dynamodb.types import TypeSerializer

from database_client import get_table, service_error_payload
from database_models import OperationResponse, UpsertRequest, normalize_document

SER = TypeSerializer()


def upsert_document(request: UpsertRequest) -> OperationResponse:
    try:
        table = get_table(request.table_name)
        item = normalize_document(dict(request.document))
        item["document_id"] = request.key.document_id
        if request.key.partition_key is not None:
            item["partition_key"] = request.key.partition_key
        table.put_item(Item=item)
        return OperationResponse(ok=True, data={"document": item})
    except Exception as exc:
        return OperationResponse(ok=False, error=service_error_payload(exc))
