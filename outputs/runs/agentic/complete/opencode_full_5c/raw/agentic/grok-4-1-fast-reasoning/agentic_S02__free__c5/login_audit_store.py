import boto3
import os
from typing import Dict, Any

dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)
table_name = os.getenv("DYNAMODB_AUDIT_TABLE_NAME")
table = dynamodb.Table(table_name)


def persist_login_audit_record(audit_record: Dict[str, Any]) -> str:
    try:
        table.put_item(Item=audit_record)
        return "success"
    except Exception as e:
        return f"failed: {str(e)}"
