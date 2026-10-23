import os
import boto3
from botocore.config import Config


def get_dynamodb_resource():
    """
    Returns a DynamoDB resource object.
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    config = Config(
        region_name=aws_region,
        signature_version="v4",
        retries={"max_attempts": 10, "mode": "standard"},
    )

    return boto3.resource(
        "dynamodb",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        config=config,
    )


def get_table(table_name="documents"):
    """
    Returns a DynamoDB table object.
    """
    dynamodb = get_dynamodb_resource()
    return dynamodb.Table(table_name)
