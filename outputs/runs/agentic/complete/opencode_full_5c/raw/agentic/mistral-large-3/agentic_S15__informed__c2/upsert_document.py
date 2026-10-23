import os
import boto3
from boto3.dynamodb.conditions import Key
from typing import Dict, Any, Optional


def get_dynamodb_table():
    """Initialize and return a DynamoDB table resource." ""
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=os.getenv("AWS_REGION", "us-west-2"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    table_name = os.getenv("DYNAMODB_TABLE_NAME", "documents")
    return dynamodb.Table(table_name)


def upsert_document(document_id: str, document: Dict[str, Any], partition_key: str = "id") -> Dict[str, Any]:
    """
    Upserts a JSON document into Amazon DynamoDB by its primary identifier.
    
    Args:
        document_id: The primary identifier of the document.
        document: The JSON document to upsert.
        partition_key: The partition key attribute name (default: "id").
        
    Returns:
        The response from DynamoDB after upserting the document.
    """
    table = get_dynamodb_table()
    document[partition_key] = document_id
    response = table.put_item(Item=document)
    return response