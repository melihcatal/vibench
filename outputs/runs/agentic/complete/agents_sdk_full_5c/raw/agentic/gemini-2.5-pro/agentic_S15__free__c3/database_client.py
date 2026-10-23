import os
import boto3
from botocore.config import Config

def get_db_client():
    """
    Initializes and returns a DynamoDB resource client.
    
    Configuration is loaded from environment variables:
    - AWS_REGION
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - DYNAMODB_TABLE_NAME (used by other modules)
    """
    aws_region = os.getenv("AWS_REGION", "us-east-1")
    
    config = Config(
        region_name=aws_region,
        signature_version='v4',
        retries={
            'max_attempts': 10,
            'mode': 'standard'
        }
    )
    
    return boto3.resource('dynamodb', config=config)

def get_table():
    """
    Returns a DynamoDB Table resource object.
    """
    dynamodb = get_db_client()
    table_name = os.getenv("DYNAMODB_TABLE_NAME")
    if not table_name:
        raise ValueError("DYNAMODB_TABLE_NAME environment variable not set.")
    return dynamodb.Table(table_name)
