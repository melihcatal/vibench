import os
import boto3
from botocore.config import Config

def get_boto_client():
    """
    Initializes and returns a Boto3 client for DynamoDB.
    """
    # Using a standard retry policy
    config = Config(
        retries={
            'max_attempts': 3,
            'mode': 'standard'
        }
    )
    
    # Credentials and region are expected to be in environment variables
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
    dynamodb_client = boto3.client(
        'dynamodb',
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        config=config
    )
    return dynamodb_client

def get_table_name():
    """
    Returns the DynamoDB table name from an environment variable.
    """
    return os.getenv("DYNAMODB_TABLE_NAME", "documents")

