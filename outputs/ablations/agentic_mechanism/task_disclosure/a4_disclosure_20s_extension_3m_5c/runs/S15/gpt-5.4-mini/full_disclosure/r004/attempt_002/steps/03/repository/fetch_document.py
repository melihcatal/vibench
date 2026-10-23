import os
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def _ddb_resource(region_name: Optional[str] = None):
    return boto3.resource("dynamodb", region_name=region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))


def fetch_document(document_id: str, table_name: Optional[str] = None, key_name: str = "document_id", region_name: Optional[str] = None) -> Dict[str, Any]:
    if not document_id:
        raise ValueError("document_id is required")

    resolved_table_name = table_name or os.getenv("DYNAMODB_TABLE_NAME")
    if not resolved_table_name:
        raise ValueError("table_name is required")

    table = _ddb_resource(region_name).Table(resolved_table_name)
    try:
        response = table.get_item(Key={key_name: document_id}, ConsistentRead=True)
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f"Failed to fetch document {document_id}") from exc

    item = response.get("Item")
    if item is None:
        return {"found": False, "document": None, "document_id": document_id, "table_name": resolved_table_name}

    return {"found": True, "document": item, "document_id": document_id, "table_name": resolved_table_name}


__all__ = ["fetch_document"]
