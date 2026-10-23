import os
import boto3
from typing import Optional

def get_db_client() -> Optional[boto3.session.Session.resource]:
    """
    Initializes and returns a Boto3 DynamoDB resource client.
    
    Credentials are sourced from environment variables:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_SESSION_TOKEN (optional)
    - AWS_DEFAULT_REGION
    """
    try:
        dynamodb = boto3.resource(
            'dynamodb',
            region_name=os.environ.get("AWS_DEFAULT_REGION"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
        )
        return dynamodb
    except Exception as e:
        print(f"Error creating DynamoDB client: {e}")
        return None

def get_db_table(table_name: str):
    """
    Returns a DynamoDB Table object.
    """
    dynamodb = get_db_client()
    if dynamodb:
        return dynamodb.Table(table_name)
    return None
