import os
import boto3
from botocore.config import Config

TABLE_NAME = os.environ.get("DYNAMODB_TABLE_NAME", "documents")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")


def get_db_client():
    config = Config(
        region_name=AWS_REGION,
        signature_version="v4",
        retries={"max_attempts": 10, "mode": "standard"},
    )
    return boto3.resource("dynamodb", config=config)


def get_db_table():
    dynamodb = get_db_client()
    return dynamodb.Table(TABLE_NAME)
