import os
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table_name = os.getenv('DYNAMODB_TABLE_NAME', 'FederatedLoginAudits')
table = dynamodb.Table(table_name)

def store_login_audit(record: dict):
    try:
        table.put_item(Item=record)
        return True
    except ClientError as e:
        print(f"Error storing audit: {e}")
        return False

def get_audit_by_id(audit_id: str):
    response = table.get_item(Key={'id': audit_id})
    return response.get('Item')

# Provider-specific: boto3 DynamoDB resource, Amazon DynamoDB