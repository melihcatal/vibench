import os
import boto3
from botocore.config import Config

# Configuration for Boto3
# It is recommended to use IAM roles or instance profiles for production environments.
# For local development, you can set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION
# in your environment variables.
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
DYNAMODB_TABLE_NAME = os.environ.get("DYNAMODB_TABLE_NAME", "documents")

# A custom configuration can be used for retries, timeouts, etc.
BOTO_CONFIG = Config(
    region_name=AWS_REGION,
    retries={
        'max_attempts': 3,
        'mode': 'standard'
    }
)

_db_resource = None

def get_db_resource():
    """Gets the DynamoDB resource singleton."""
    global _db_resource
    if not _db_resource:
        _db_resource = boto3.resource('dynamodb', config=BOTO_CONFIG)
    return _db_resource

def get_db_table():
    """Gets the DynamoDB Table object."""
    dynamodb = get_db_resource()
    return dynamodb.Table(DYNAMODB_TABLE_NAME)
