import os
import boto3
from botocore.exceptions import ClientError
from identity_models import AuditEvent
from dataclasses import asdict


def persist_login_audit(event: AuditEvent):
    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )
    table_name = os.getenv("DYNAMODB_TABLE_NAME", "FederatedLoginAudits")
    table = dynamodb.Table(table_name)
    try:
        table.put_item(Item=asdict(event))
        print(f"Persisted audit event {event.id} to Amazon DynamoDB table {table_name}")
    except ClientError as e:
        print(f"Failed to persist audit to DynamoDB: {e}")


if __name__ == "__main__":
    pass
