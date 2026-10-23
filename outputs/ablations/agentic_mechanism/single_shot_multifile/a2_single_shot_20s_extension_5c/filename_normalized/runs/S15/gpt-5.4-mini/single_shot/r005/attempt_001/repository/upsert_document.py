import os
from typing import Any, Dict
import boto3
from botocore.exceptions import ClientError
from database_client import get_dynamodb_table
from database_models import DocumentUpsertRequest, DocumentUpsertResponse, normalize_document


def upsert_document(payload: Dict[str, Any]) -> Dict[str, Any]:
    request = DocumentUpsertRequest.from_dict(payload)
    table = get_dynamodb_table()
    item = normalize_document(request.document)
    item[request.primary_key_name] = request.primary_key_value
    if request.version is not None:
        item[request.version_field] = request.version
    table.put_item(Item=item)
    return DocumentUpsertResponse(
        ok=True,
        primary_key_name=request.primary_key_name,
        primary_key_value=request.primary_key_value,
        document=item,
    ).to_dict()


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    return upsert_document(event)
