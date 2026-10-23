import os
from typing import Dict, Any
import boto3

# Using Amazon DynamoDB as the managed NoSQL document store
# Provider identified by the boto3 import and AWS credentials

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
if not (AWS_ACCESS_KEY and AWS_SECRET_KEY):
    raise RuntimeError('Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables')

dynamodb = boto3.resource('dynamodb', aws_access_key_id=AWS_ACCESS_KEY,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                          region_name='us-east-1')

TABLE_NAME = 'message-audit'  # concrete table identifier

def create_audit_table_if_missing():
    try:
        dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[{'AttributeName': 'message_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'message_id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        print(f'Ensured DynamoDB table {TABLE_NAME} exists.')
    except dynamodb.meta.client.exceptions.ResourceInUseException:
        print(f'Table {TABLE_NAME} already exists.')

def store_processed_message(record: Dict[str, Any]):
    """Persist a processed message record for later lookup.

    The record must include a unique 'message_id' field.
    Additional fields are stored as attributes.
    """
    table = dynamodb.Table(TABLE_NAME)
    # Ensure the shape expected by DynamoDB (string values only)
    item = {k: str(v) for k, v in record.items()}
    table.put_item(Item=item)
    print(f'Stored audit record for message_id={record.get("message_id")}')

def main():
    sample_record = {
        'message_id': 'msg-20250827-001',
        'timestamp': '2025-08-27T12:30:00Z',
        'status': 'processed',
        'content_hash': 'abc123',
        'topic': 'my-topic'
    }
    create_audit_table_if_missing()
    store_processed_message(sample_record)

if __name__ == '__main__':
    main()
