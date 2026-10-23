import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError


@dataclass
class UpsertResult:
    document_id: str
    created: bool
    updated: bool
    version: Optional[str]
    record: Dict[str, Any]


def _ddb_table_name() -> str:
    table_name = os.getenv("AWS_DYNAMODB_TABLE_NAME") or os.getenv("DYNAMODB_TABLE_NAME")
    if not table_name:
        raise ValueError("Missing AWS_DYNAMODB_TABLE_NAME")
    return table_name


def _ddb_client():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    return boto3.resource("dynamodb", region_name=region).Table(_ddb_table_name())


def _normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(document, dict):
        raise TypeError("document must be a JSON object")
    if "id" in document:
        doc_id = document["id"]
    elif "document_id" in document:
        doc_id = document["document_id"]
        document["id"] = doc_id
    else:
        raise ValueError('document must include "id" or "document_id"')
    if not isinstance(doc_id, (str, int)) or doc_id == "":
        raise ValueError("document id must be a non-empty string or integer")
    return document


def upsert_document(document: Dict[str, Any]) -> UpsertResult:
    table = _ddb_client()
    normalized = _normalize_document(dict(document))
    doc_id = str(normalized["id"])
    version = normalized.get("version")
    update_expr = "SET #doc = :doc, updated_at = :updated_at"
    expr_names = {"#doc": "document"}
    expr_values = {":doc": normalized, ":updated_at": normalized.get("updated_at") or ""}
    if version is not None:
        update_expr += ", version = :version"
        expr_values[":version"] = version
    try:
        response = table.update_item(
            Key={"id": doc_id},
            UpdateExpression=update_expr,
            ExpressionAttributeNames=expr_names,
            ExpressionAttributeValues=expr_values,
            ReturnValues="ALL_NEW",
        )
        record = response.get("Attributes", {})
        return UpsertResult(
            document_id=doc_id,
            created=False,
            updated=True,
            version=str(record.get("version")) if record.get("version") is not None else None,
            record=record,
        )
    except ClientError as exc:
        if exc.response.get("Error", {}).get("Code") not in {"ConditionalCheckFailedException", "ValidationException"}:
            raise
        response = table.put_item(Item=normalized)
        if response.get("ResponseMetadata", {}).get("HTTPStatusCode") not in {200, 201}:  # pragma: no cover
            raise RuntimeError("failed to upsert document")
        return UpsertResult(
            document_id=doc_id,
            created=True,
            updated=False,
            version=str(version) if version is not None else None,
            record=normalized,
        )


def upsert_document_from_json(payload: str) -> UpsertResult:
    return upsert_document(json.loads(payload))


__all__ = ["UpsertResult", "upsert_document", "upsert_document_from_json"]
