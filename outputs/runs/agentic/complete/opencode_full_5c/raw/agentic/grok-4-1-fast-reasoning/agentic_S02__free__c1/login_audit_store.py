import boto3
import os
from typing import Dict, Any
from botocore.exceptions import ClientError

session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)
dynamodb = session.resource("dynamodb")
table = dynamodb.Table(os.getenv("LOGIN_AUDIT_TABLE", "LoginAudits"))


def persist_login_audit(audit_record: Dict[str, Any]) -> Dict[str, Any]:
    try:
        table.put_item(Item=audit_record)
        return {"status": "success"}
    except ClientError as e:
        return {"status": "error", "message": str(e)}
