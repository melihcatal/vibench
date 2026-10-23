import os
import boto3
from botocore.exceptions import ClientError
from identity_models import AuditEvent
import json
from decimal import Decimal

class AuditEventEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super(AuditEventEncoder, self).default(obj)


def persist_audit_event(event: AuditEvent):
    """
    Persists a federated login audit event to Amazon DynamoDB.
    """
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    table_name = os.environ.get("DYNAMODB_AUDIT_TABLE", "federated-login-audit")
    table = dynamodb.Table(table_name)
    
    try:
        item = json.loads(json.dumps(event.__dict__), parse_float=Decimal)
        
        response = table.put_item(Item=item)
        return response
    except ClientError as e:
        print(f"Error persisting event to DynamoDB: {e.response['Error']['Message']}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
