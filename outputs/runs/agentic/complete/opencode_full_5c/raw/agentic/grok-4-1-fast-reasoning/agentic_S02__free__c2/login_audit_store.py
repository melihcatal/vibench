import os
import boto3
from dataclasses import asdict
from identity_models import AuditEvent

dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)
table = dynamodb.Table(os.getenv("AUDIT_TABLE_NAME", "FederatedLoginAudits"))


def login_audit_store(event: AuditEvent):
    table.put_item(Item=asdict(event))
