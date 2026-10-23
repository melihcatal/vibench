import os
import boto3
from botocore.config import Config

def get_db_client():
    """
    Initializes and returns a DynamoDB resource client.
    
    Provider: AWS DynamoDB
    """
    # Boto3 automatically uses credentials from environment variables 
    # (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN) or an IAM role.
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    
    config = Config(
        region_name=aws_region,
        signature_version='v4',
        retries={'max_attempts': 10, 'mode': 'standard'}
    )
    
    return boto3.resource('dynamodb', config=config)

def get_db_table(table_name: str = None):
    """
    Returns a DynamoDB Table resource object.
    
    The table name is retrieved from the DYNAMODB_TABLE_NAME environment
    variable if not provided.
    """
    dynamodb_resource = get_db_client()
    
    resolved_table_name = table_name or os.environ.get("DYNAMODB_TABLE_NAME")
    if not resolved_table_name:
        raise ValueError("DYNAMODB_TABLE_NAME environment variable not set and no table_name provided.")
        
    return dynamodb_resource.Table(resolved_table_name)
