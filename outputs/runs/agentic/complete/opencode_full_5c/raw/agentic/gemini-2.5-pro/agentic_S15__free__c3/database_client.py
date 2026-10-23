import os
import boto3


def get_database_client():
    """
    Initializes and returns a DynamoDB client.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.resource("dynamodb", region_name=region_name)


def get_table_name():
    """
    Returns the DynamoDB table name from environment variables.
    """
    return os.environ.get("DYNAMODB_TABLE_NAME", "documents")
