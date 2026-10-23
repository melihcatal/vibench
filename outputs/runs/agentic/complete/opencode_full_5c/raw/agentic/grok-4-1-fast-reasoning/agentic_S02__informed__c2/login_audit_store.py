import boto3
import os
from identity_models import AuditEvent

dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
)

table = dynamodb.Table("FederatedLoginAudits")


def persist_login_audit(event: AuditEvent) -> None:
    table.put_item(Item=event.to_dict())
