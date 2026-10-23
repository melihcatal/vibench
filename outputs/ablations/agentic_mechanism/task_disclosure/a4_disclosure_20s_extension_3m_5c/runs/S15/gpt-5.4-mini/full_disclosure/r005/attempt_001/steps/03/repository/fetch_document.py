import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError


@dataclass
class FetchResult:
    document_id: str
    found: bool
    record: Optional[Dict[str, Any]]


def _ddb_table_name() -> str:
    table_name = os.getenv("AWS_DYNAMODB_TABLE_NAME") or os.getenv("DYNAMODB_TABLE_NAME")
    if not table_name:
        raise ValueError("Missing AWS_DYNAMODB_TABLE_NAME")
    return table_name


def _ddb_table():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    return boto3.resource("dynamodb", region_name=region).Table(_ddb_table_name())


def fetch_document(document_id: Any) -> FetchResult:
    if document_id is None or document_id == "":
        raise ValueError("document_id must be provided")
    table = _ddb_table()
    doc_id = str(document_id)
    try:
        response = table.get_item(Key={"id": doc_id})
    except ClientError:
        raise
    record = response.get("Item")
    return FetchResult(document_id=doc_id, found=record is not None, record=record)


__all__ = ["FetchResult", "fetch_document"]
