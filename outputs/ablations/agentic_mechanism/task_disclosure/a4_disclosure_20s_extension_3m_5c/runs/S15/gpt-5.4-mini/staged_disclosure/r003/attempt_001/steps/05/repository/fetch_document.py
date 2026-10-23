import json
import os
import sys

import boto3
from botocore.exceptions import ClientError


def fetch_document(document_id: str):
    table_name = os.environ["DYNAMODB_TABLE_NAME"]
    region = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))
    dynamodb = boto3.resource("dynamodb", region_name=region)
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={"document_id": document_id})
    return response.get("Item")


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: fetch_document.py <document_id>")
    try:
        document = fetch_document(sys.argv[1])
    except ClientError as exc:
        raise SystemExit(str(exc)) from exc
    print(json.dumps(document, default=str))


if __name__ == "__main__":
    main()
