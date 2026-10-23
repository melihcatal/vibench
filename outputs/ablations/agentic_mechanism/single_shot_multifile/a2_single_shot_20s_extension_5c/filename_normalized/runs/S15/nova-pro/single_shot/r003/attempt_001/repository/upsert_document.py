import boto3
from database_client import get_dynamodb_client

def upsert_document(document):
    client = get_dynamodb_client()
    response = client.put_item(
        TableName='Documents',
        Item=document
    )
    return response