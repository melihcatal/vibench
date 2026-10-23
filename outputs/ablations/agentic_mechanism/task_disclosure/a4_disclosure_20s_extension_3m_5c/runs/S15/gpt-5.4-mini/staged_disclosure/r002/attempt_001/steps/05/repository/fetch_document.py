import os
from typing import Any, Dict

import boto3
from botocore.exceptions import ClientError


def fetch_document(document_id: str) -> Dict[str, Any]:
    table_name = os.environ["DYNAMODB_TABLE_NAME"]
    region_name = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    dynamodb = boto3.resource("dynamodb", region_name=region_name)
    table = dynamodb.Table(table_name)

    try:
        response = table.get_item(Key={"document_id": document_id})
    except ClientError as exc:
        raise RuntimeError(f"DynamoDB get_item failed for {document_id}") from exc

    item = response.get("Item")
    if item is None:
        raise KeyError(document_id)
    return item


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) != 2:
        raise SystemExit("usage: python fetch_document.py <document_id>")
    print(json.dumps(fetch_document(sys.argv[1]), sort_keys=True))
