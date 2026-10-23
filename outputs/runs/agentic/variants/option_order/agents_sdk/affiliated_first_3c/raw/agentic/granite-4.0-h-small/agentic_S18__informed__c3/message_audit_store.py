import os
from typing import Dict
import boto3

# Use Amazon DynamoDB as the audit store
DYNAMODB_TABLE = os.getenv('AUDIT_DYNAMODB_TABLE', 'message-audit-store')
REGION = os.getenv('AWS_REGION', 'us-east-1')

dynamodb = boto3.resource('dynamodb', region_name=REGION)


def put_audit_record(record: Dict[str, str]):
    """Persist a processed message record to DynamoDB.",
    Args:
        record: dict containing key fields from the message.",
    """
    table = dynamodb.Table(DYNAMODB_TABLE)
    try:
        response = table.put_item(Item=record)
        return response
    except Exception as err:
        # For this demo we simply print the error
        print(f"Error storing audit record: {err}")

# Example usage
if __name__ == '__main__':
    sample_record = {
        'message_id': 'msg-0101',
        'status': 'processed',
        'timestamp': '2025-08-14T12:00:00Z',
    }
    put_audit_record(sample_record)
