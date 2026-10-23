import boto3
import os
from typing import Dict, Any, Union
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer

def get_dynamodb_client():
    """
    Initializes and returns a boto3 DynamoDB client.
    Uses environment variables for configuration.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    dynamodb_client = boto3.client(
        "dynamodb",
        region_name=region_name,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )
    return dynamodb_client

def get_table_name() -> str:
    """
    Returns the DynamoDB table name from environment variables.
    """
    table_name = os.environ.get("DYNAMODB_TABLE_NAME")
    if not table_name:
        raise ValueError("DYNAMODB_TABLE_NAME environment variable not set.")
    return table_name

_serializer = TypeSerializer()
_deserializer = TypeDeserializer()

def serialize_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """Serializes a Python dict into DynamoDB attribute value format."""
    return {k: _serializer.serialize(v) for k, v in item.items()}

def deserialize_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """Deserializes a DynamoDB attribute value format into a Python dict."""
    return {k: _deserializer.deserialize(v) for k, v in item.items()}
