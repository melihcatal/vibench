import os
import boto3
from messaging_models import Event

dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)
table_name = os.getenv("AUDIT_TABLE_NAME", "MessageAudits")
table = dynamodb.Table(table_name)


def store_audit_record(event: Event):
    table.put_item(
        Item={
            "id": event.id,
            "event_type": event.event_type,
            "payload": event.payload,
            "timestamp": event.timestamp,
        }
    )
