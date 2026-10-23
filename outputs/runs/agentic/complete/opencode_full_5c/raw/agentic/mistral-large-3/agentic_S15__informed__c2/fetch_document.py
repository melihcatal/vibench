import os
import boto3
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


def fetch_document(document_id: str, partition_key: str = "id") -> Optional[Dict[str, Any]]:
    """
    Fetches a document from Amazon DynamoDB by its primary identifier.
    
    Args:
        document_id: The primary identifier of the document.
        partition_key: The partition key attribute name (default: "id").
        
    Returns:
        The fetched document as a dictionary, or None if not found.
    """
    table = get_dynamodb_table()
    response = table.get_item(Key={partition_key: document_id})
    return response.get("Item")