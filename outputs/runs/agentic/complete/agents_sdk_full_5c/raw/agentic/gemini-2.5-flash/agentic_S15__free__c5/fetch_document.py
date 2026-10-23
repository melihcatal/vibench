import boto3
import os
from database_client import get_dynamodb_client

def fetch_document(table_name: str, key: dict):
    """
    Fetches a document from a DynamoDB table by its primary key.
    The 'key' dictionary should contain the primary key attribute names and values.
    """
    dynamodb = get_dynamodb_client()
    try:
        response = dynamodb.get_item(
            TableName=table_name,
            Key=key
        )
        return response.get('Item')
    except Exception as e:
        print(f"Error fetching document: {e}")
        raise
