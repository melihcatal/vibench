import os
from typing import Any, Dict, List, Optional

import boto3
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError


def _table_name(table_name: Optional[str]) -> str:
    resolved = table_name or os.environ.get("DYNAMODB_TABLE_NAME")
    if not resolved:
        raise ValueError("table_name is required")
    return resolved


def _region_name(region_name: Optional[str]) -> Optional[str]:
    return region_name or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")


def query_documents(
    field_name: str,
    field_value: Any,
    table_name: Optional[str] = None,
    region_name: Optional[str] = None,
    partition_key_name: Optional[str] = None,
) -> List[Dict[str, Any]]:
    if not field_name:
        raise ValueError("field_name is required")

    table_name = _table_name(table_name)
    region_name = _region_name(region_name)

    dynamodb = boto3.resource("dynamodb", region_name=region_name)
    table = dynamodb.Table(table_name)

    try:
        if partition_key_name and field_name == partition_key_name:
            response = table.query(KeyConditionExpression=Key(field_name).eq(field_value))
        else:
            response = table.scan(FilterExpression=Attr(field_name).eq(field_value))
    except ClientError as exc:
        raise RuntimeError(
            f"Failed to query documents by {field_name}: {exc.response['Error'].get('Message', str(exc))}"
        ) from exc

    return response.get("Items", [])


def main() -> None:
    import json
    import sys

    if len(sys.argv) < 3:
        raise SystemExit("usage: query_documents.py <field-name> <field-value>")
    result = query_documents(sys.argv[1], sys.argv[2])
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
