import boto3
from database_client import get_dynamodb_client

def upsert_document(table_name, item):
    dynamodb = get_dynamodb_client()
    response = dynamodb.put_item(
        TableName=table_name,
        Item=item
    )
    return response