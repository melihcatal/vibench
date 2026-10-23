import boto3
from database_client import get_dynamodb_client

def fetch_document(document_id):
    client = get_dynamodb_client()
    response = client.get_item(
        TableName='Documents',
        Key={'id': {'S': document_id}}
    )
    return response['Item'] if 'Item' in response else None