import os
import boto3
from botocore.config import Config


def get_db_client():
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS credentials are not configured in environment variables.")

    config = Config(
        region_name=aws_region,
        signature_version="v4",
        retries={"max_attempts": 10, "mode": "standard"},
    )

    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        config=config,
    )
    return dynamodb


def get_db_table(table_name="documents"):
    dynamodb = get_db_client()
    return dynamodb.Table(table_name)
