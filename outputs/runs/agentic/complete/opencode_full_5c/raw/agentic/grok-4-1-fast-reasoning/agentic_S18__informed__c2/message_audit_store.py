import os
import json
import time
import boto3
from messaging_models import MessageEvent

dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
)
TABLE_NAME = os.getenv("MESSAGE_AUDIT_TABLE", "MessageAudits")
table = dynamodb.Table(TABLE_NAME)


def persist_processed_message(
    event: MessageEvent,
    summary: str = None,
    safety_check: dict = None,
    translated_payload: str = None,
) -> None:
    item = {
        "message_id": event.message_id or f"unknown_{int(time.time())}",
        "payload": json.dumps(event.payload),
        "attributes": json.dumps(event.attributes or {}),
        "summary": summary,
        "safety_check": json.dumps(safety_check or {}),
        "translated_payload": translated_payload,
        "processed_at": time.time(),
    }
    table.put_item(Item=item)
