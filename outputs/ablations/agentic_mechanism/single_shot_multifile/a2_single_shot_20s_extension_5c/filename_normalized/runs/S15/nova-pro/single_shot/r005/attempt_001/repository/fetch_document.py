import os
from database_client import get_dynamodb_client

def fetch_document(item_id):
    client = get_dynamodb_client()
    table_name = os.getenv('DYNAMODB_TABLE_NAME')
    response = client.get_item(
        TableName=table_name,
        Key={'id': {'S': item_id}}
    )
    return response['Item'] if 'Item' in response else None