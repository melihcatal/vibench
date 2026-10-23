import json
import sys
from typing import Any

import boto3
from boto3.dynamodb.conditions import Attr, Key

from database_client import load_database_config
from database_models import normalize_value


def query_documents(field_name: str, field_value: Any):
    config = load_database_config()
    table = boto3.resource("dynamodb", region_name=config.region_name).Table(
        config.table_name
    )
    normalized = normalize_value(field_value)
    if field_name == "partition_key":
        response = table.query(
            KeyConditionExpression=Key("partition_key").eq(normalized)
        )
    else:
        response = table.scan(FilterExpression=Attr(field_name).eq(normalized))
    return response.get("Items", [])


def main() -> None:
    payload = json.loads(sys.stdin.read())
    result = query_documents(payload["field_name"], payload["field_value"])
    sys.stdout.write(json.dumps(result, default=str))


if __name__ == "__main__":
    main()
