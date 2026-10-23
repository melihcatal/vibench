import json
import os
import sys

import boto3
from boto3.dynamodb.conditions import Key, Attr

from database_client import get_table, get_table_name, get_region
from database_models import build_error_response, build_success_response


def query_documents(field_name, field_value, partition_key_name=None):
    table = get_table()
    if partition_key_name:
        result = table.query(
            KeyConditionExpression=Key(partition_key_name).eq(field_value)
        )
    else:
        result = table.scan(FilterExpression=Attr(field_name).eq(field_value))
    return build_success_response(
        item={"items": result.get("Items", [])}, message="queried"
    )


def main():
    try:
        payload = json.loads(sys.stdin.read())
        print(
            json.dumps(
                query_documents(
                    payload["field_name"],
                    payload["field_value"],
                    payload.get("partition_key_name"),
                )
            )
        )
    except Exception as exc:
        print(json.dumps(build_error_response(exc)))


if __name__ == "__main__":
    main()
