import os
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError


def fetch_document(document_id: str, table_name: Optional[str] = None, region_name: Optional[str] = None) -> Dict[str, Any]:
    table_name = table_name or os.environ.get("DYNAMODB_TABLE_NAME")
    region_name = region_name or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    if not table_name:
        raise ValueError("table_name is required")
    if not document_id:
        raise ValueError("document_id is required")
    dynamodb = boto3.resource("dynamodb", region_name=region_name)
    table = dynamodb.Table(table_name)
    try:
        response = table.get_item(Key={"document_id": document_id})
    except ClientError as exc:
        raise RuntimeError(f"Failed to fetch document {document_id}: {exc.response['Error'].get('Message', str(exc))}") from exc
    item = response.get("Item")
    if item is None:
        raise KeyError(f"Document not found: {document_id}")
    return item
