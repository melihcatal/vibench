import os
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any

dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1")
)
TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "FederatedLoginAudits")
table = dynamodb.Table(TABLE_NAME)

def store_login_audit(audit_record: Dict[str, Any]) -> bool:
    try:
        table.put_item(Item=audit_record)
        return True
    except ClientError as e:
        print(f"AWS Error storing audit: {e}")
        return False