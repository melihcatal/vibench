import json
import os
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def fetch_document(identifier: str, table_name: Optional[str] = None, region_name: Optional[str] = None) -> Dict[str, Any]:
    if not identifier:
        raise ValueError("identifier is required")

    table_name = table_name or os.environ.get("DYNAMODB_TABLE_NAME")
    if not table_name:
        raise ValueError("table_name is required")

    session = boto3.Session(region_name=region_name or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"))
    client = session.resource("dynamodb")
    table = client.Table(table_name)

    try:
        response = table.get_item(Key={"id": identifier})
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f"Failed to fetch document from Amazon DynamoDB: {exc}") from exc

    item = response.get("Item")
    if item is None:
        raise KeyError(f"Document not found for identifier: {identifier}")
    return item


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("Usage: python fetch_document.py <identifier> [table_name]")

    doc = fetch_document(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    print(json.dumps(doc, default=str))
