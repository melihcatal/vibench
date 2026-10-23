import os
from typing import Any, Dict, List, Optional

import boto3
from boto3.dynamodb.conditions import Attr, Key


class QueryDocumentsError(Exception):
    pass


def _table_name() -> str:
    name = os.environ.get("AWS_DYNAMODB_TABLE_NAME") or os.environ.get("DYNAMODB_TABLE_NAME")
    if not name:
        raise QueryDocumentsError("Missing table name")
    return name


def _table():
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    kwargs: Dict[str, Any] = {}
    if region:
        kwargs["region_name"] = region
    resource = boto3.resource("dynamodb", **kwargs)
    return resource.Table(_table_name())


def query_documents(
    field_name: str,
    field_value: Any,
    *,
    partition_key_name: Optional[str] = None,
    limit: Optional[int] = None,
    consistent_read: bool = False,
) -> List[Dict[str, Any]]:
    table = _table()
    if partition_key_name and field_name == partition_key_name:
        kwargs: Dict[str, Any] = {
            "KeyConditionExpression": Key(field_name).eq(field_value),
            "ConsistentRead": consistent_read,
        }
        if limit is not None:
            kwargs["Limit"] = limit
        response = table.query(**kwargs)
        return response.get("Items", [])

    kwargs = {
        "FilterExpression": Attr(field_name).eq(field_value),
        "ConsistentRead": consistent_read,
    }
    if limit is not None:
        kwargs["Limit"] = limit
    response = table.scan(**kwargs)
    return response.get("Items", [])


def main() -> None:
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Query documents from Amazon DynamoDB")
    parser.add_argument("field_name")
    parser.add_argument("field_value")
    parser.add_argument("--partition-key-name")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--consistent-read", action="store_true")
    args = parser.parse_args()
    result = query_documents(
        args.field_name,
        args.field_value,
        partition_key_name=args.partition_key_name,
        limit=args.limit,
        consistent_read=args.consistent_read,
    )
    print(json.dumps(result, default=str))


if __name__ == "__main__":
    main()
