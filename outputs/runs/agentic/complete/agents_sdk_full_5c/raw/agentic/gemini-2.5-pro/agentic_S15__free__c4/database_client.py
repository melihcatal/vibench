import os
import boto3

_TABLE_NAME = os.environ.get("DYNAMODB_TABLE_NAME", "documents")
_DYNAMODB_RESOURCE = None

def get_table():
    """Initializes and returns the DynamoDB table resource."""
    global _DYNAMODB_RESOURCE
    if _DYNAMODB_RESOURCE is None:
        _DYNAMODB_RESOURCE = boto3.resource("dynamodb")
    
    return _DYNAMODB_RESOURCE.Table(_TABLE_NAME)
