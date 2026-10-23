import os
import boto3
from botocore.config import Config

DYNAMODB_TABLE_NAME = os.environ.get("DYNAMODB_TABLE_NAME", "documents")

def get_dynamodb_resource():
    """
    Initializes and returns a Boto3 DynamoDB resource client.
    """
    # For local testing with DynamoDB Local, you might use:
    # endpoint_url = os.environ.get("DYNAMODB_ENDPOINT_URL")
    # if endpoint_url:
    #     return boto3.resource(
    #         "dynamodb",
    #         endpoint_url=endpoint_url,
    #         region_name=os.environ.get("AWS_REGION", "us-east-1"),
    #         aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", "fake"),
    #         aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", "fake"),
    #     )

    return boto3.resource(
        "dynamodb",
        region_name=os.environ.get("AWS_REGION"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        config=Config(
            retries={"max_attempts": 3, "mode": "standard"}
        ),
    )

def get_dynamodb_table():
    """
    Returns a DynamoDB table object.
    """
    dynamodb_resource = get_dynamodb_resource()
    return dynamodb_resource.Table(DYNAMODB_TABLE_NAME)
