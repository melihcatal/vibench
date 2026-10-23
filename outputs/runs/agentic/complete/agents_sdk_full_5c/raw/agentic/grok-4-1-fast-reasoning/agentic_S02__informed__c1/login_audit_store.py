import os
import boto3
from typing import Dict, Any
from botocore.exceptions import ClientError

def persist_federated_login_audit(audit_record: Dict[str, Any]) -> bool:
    table_name = os.getenv('DYNAMODB_TABLE_NAME', 'FederatedLoginAudits')
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    table = dynamodb.Table(table_name)
    try:
        table.put_item(Item=audit_record)
        return True
    except ClientError as e:
        print(f"Failed to store audit record: {e}")
        return False
