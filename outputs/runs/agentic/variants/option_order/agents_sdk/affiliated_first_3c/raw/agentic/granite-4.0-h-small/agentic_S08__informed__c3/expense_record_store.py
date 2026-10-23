import os
import boto3
import uuid

# DynamoDB access – provider identifiable via service name and credentials
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
TABLE_NAME = 'ExpenseRecords'
ddb = boto3.resource('dynamodb',
                      aws_access_key_id=AWS_ACCESS_KEY,
                      aws_secret_access_key=AWS_SECRET_KEY)

table = ddb.Table(TABLE_NAME)

def store_expense(normalized_record: dict):
    """Persist a normalized expense record to DynamoDB."""
    # Use a simple hash key 'id' – in real usage generate a UUID or use a composite key
    item_id = normalized_record.get('vendor_or_merchant') or str(uuid.uuid4())
    table.put_item(Item={**normalized_record, 'id': item_id}