import os
from typing import Any, Dict, Optional

import boto3


def fetch_document(document_id: str, table_name: Optional[str] = None) -> Dict[str, Any]:
    if not document_id:
        raise ValueError("document_id is required")
    table = table_name or os.environ.get("DYNAMODB_TABLE_NAME")
    if not table:
        raise ValueError("table_name or DYNAMODB_TABLE_NAME is required")
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    dynamodb = boto3.resource("dynamodb", region_name=region)
    result = dynamodb.Table(table).get_item(Key={"document_id": document_id})
    item = result.get("Item")
    if item is None:
        raise KeyError(document_id)
    return item
