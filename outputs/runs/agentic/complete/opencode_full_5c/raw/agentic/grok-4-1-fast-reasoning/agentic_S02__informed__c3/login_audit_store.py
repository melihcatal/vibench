import boto3
import os
from identity_models import AuditEvent


def store_login_audit_record(table_name: str, event: AuditEvent) -> None:
    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    )
    table = dynamodb.Table(table_name)
    item = {
        "event_id": event.event_id,
        "timestamp": event.timestamp,
        "event_type": event.event_type,
        "user_id": event.user_id or "",
        "success": event.success,
    }
    table.put_item(Item=item)
