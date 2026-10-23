import os
import boto3
from botocore.config import Config


def get_db_client():
    return boto3.resource(
        "dynamodb",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        config=Config(retries={"max_attempts": 10, "mode": "standard"}),
    )


def get_db_table():
    dynamodb = get_db_client()
    return dynamodb.Table(os.environ.get("DYNAMODB_TABLE_NAME", "documents"))
