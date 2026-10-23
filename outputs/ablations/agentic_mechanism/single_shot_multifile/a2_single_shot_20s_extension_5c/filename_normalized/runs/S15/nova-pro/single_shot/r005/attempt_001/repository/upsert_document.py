import os
from database_client import get_dynamodb_client

def upsert_document(item):
    client = get_dynamodb_client()
    table_name = os.getenv('DYNAMODB_TABLE_NAME')
    response = client.put_item(
        TableName=table_name,
        Item=item
    )
    return response