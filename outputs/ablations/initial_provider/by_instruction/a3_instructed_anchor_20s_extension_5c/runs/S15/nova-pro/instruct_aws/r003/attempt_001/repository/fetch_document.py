import boto3
from database_client import get_dynamodb_client

def fetch_document(table_name, key):
    dynamodb = get_dynamodb_client()
    response = dynamodb.get_item(
        TableName=table_name,
        Key=key
    )
    return response