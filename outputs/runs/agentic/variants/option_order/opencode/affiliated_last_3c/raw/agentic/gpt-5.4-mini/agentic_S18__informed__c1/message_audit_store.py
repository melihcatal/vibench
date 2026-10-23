import os
import boto3
from datetime import datetime, timezone


def persist_message_record(record: dict) -> dict:
    dynamodb = boto3.resource(
        "dynamodb", region_name=os.getenv("AWS_REGION", "us-east-1")
    )
    table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])
    item = {
        "message_id": record.get("message_id", ""),
        "created_at": datetime.now(timezone.utc).isoformat(),
        **record,
    }
    table.put_item(Item=item)
    return {
        "provider": "amazon-dynamodb",
        "table": os.environ["DYNAMODB_TABLE"],
        "message_id": item["message_id"],
    }
