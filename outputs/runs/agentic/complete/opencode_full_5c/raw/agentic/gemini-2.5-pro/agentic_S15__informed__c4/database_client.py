import os
import boto3
from botocore.config import Config

TABLE_NAME = os.environ.get("DYNAMODB_TABLE_NAME", "documents")


def get_db_resource():
    return boto3.resource(
        "dynamodb",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        config=Config(retries={"max_attempts": 3, "mode": "standard"}),
    )


def get_db_table():
    dynamodb = get_db_resource()
    return dynamodb.Table(TABLE_NAME)
