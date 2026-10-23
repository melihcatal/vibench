from __future__ import annotations

import os
from typing import Any

from boto3 import resource

from messaging_models import normalize_processing_record


DYNAMODB_TABLE_ENV = "AWS_DYNAMODB_AUDIT_TABLE"


def store_processed_message(record: dict[str, Any]) -> dict[str, Any]:
    table_name = os.getenv(DYNAMODB_TABLE_ENV)
    if not table_name:
        raise RuntimeError(
            f"Missing required environment variable: {DYNAMODB_TABLE_ENV}"
        )
    dynamodb = resource("dynamodb", region_name=os.getenv("AWS_REGION", "us-east-1"))
    table = dynamodb.Table(table_name)
    item = normalize_processing_record(record)
    if "message_id" not in item:
        raise ValueError("record must include message_id")
    table.put_item(Item=item)
    return {
        "provider": "aws-dynamodb",
        "table": table_name,
        "region": os.getenv("AWS_REGION", "us-east-1"),
        "message_id": item["message_id"],
        "stored": True,
    }
