import os
import boto3
from botocore.exceptions import ClientError
import json

def persist_login_audit(audit_record: dict, table_name: str = "FederatedLoginAudits"):
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    )
    table = dynamodb.Table(table_name)
    try:
        table.put_item(Item=json.loads(json.dumps(audit_record)))  # ensure serializable
        print("Audit record persisted.")
    except ClientError as e:
        raise Exception(f"Failed to store audit: {e}")