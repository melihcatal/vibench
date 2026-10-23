import boto3
import os
from database_client import get_dynamodb_client

def upsert_document(table_name: str, document: dict):
    """
    Upserts a JSON document into a DynamoDB table.
    The document must contain the primary key of the table.
    """
    dynamodb = get_dynamodb_client()
    try:
        response = dynamodb.put_item(
            TableName=table_name,
            Item=document
        )
        return response
    except Exception as e:
        print(f"Error upserting document: {e}")
        raise
