import os
import boto3
from boto3.dynamodb.conditions import Key
from typing import Dict, Any, List, Optional


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


def query_documents(
    field_name: str, 
    field_value: Any, 
    index_name: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Queries documents in Amazon DynamoDB by a field value or partition-style key.
    
    Args:
        field_name: The name of the field to query.
        field_value: The value of the field to match.
        index_name: The name of the secondary index to use (optional).
        
    Returns:
        A list of matching documents.
    """
    table = get_dynamodb_table()
    
    if index_name:
        response = table.query(
            IndexName=index_name,
            KeyConditionExpression=Key(field_name).eq(field_value)
        )
    else:
        response = table.query(
            KeyConditionExpression=Key(field_name).eq(field_value)
        )
    
    return response.get("Items", [])