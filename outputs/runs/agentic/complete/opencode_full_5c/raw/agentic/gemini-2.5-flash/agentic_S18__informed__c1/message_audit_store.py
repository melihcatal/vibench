import os
import boto3
import datetime
from messaging_models import AuditRecord


def persist_audit_record(table_name: str, record: AuditRecord):
    dynamodb_client = boto3.client(
        "dynamodb",
        region_name=os.environ.get("AWS_REGION"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    item = {
        "record_id": {"S": record["record_id"]},
        "original_message_id": {"S": record["original_message_id"]},
        "timestamp": {"S": record["timestamp"]},
        "status": {"S": record["status"]},
        "processing_details": {"S": str(record["processing_details"])},
    }

    response = dynamodb_client.put_item(TableName=table_name, Item=item)
    return response
