import os
import boto3


def get_dynamodb_client():
    """Initializes and returns the DynamoDB client."""
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not all([aws_access_key_id, aws_secret_access_key]):
        raise ValueError("AWS credentials are not configured in environment variables.")

    dynamodb = boto3.resource(
        "dynamodb",
        region_name=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    return dynamodb


def get_table(table_name="documents"):
    """Returns a DynamoDB table resource."""
    dynamodb = get_dynamodb_client()
    return dynamodb.Table(table_name)
