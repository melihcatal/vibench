import os
import boto3
from botocore.config import Config

def get_dynamodb_table():
    """
    Initializes and returns a DynamoDB table resource.
    """
    table_name = os.environ.get("DYNAMODB_TABLE_NAME")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not table_name:
        raise ValueError("DYNAMODB_TABLE_NAME environment variable not set.")

    # Using a standard Boto3 session
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=aws_region,
        config=Config(
            retries={
                'max_attempts': 3,
                'mode': 'standard'
            }
        )
    )
    
    return dynamodb.Table(table_name)

def get_boto3_client(service_name: str):
    """
    Initializes and returns a Boto3 client for a given service.
    """
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client(service_name, region_name=aws_region)
