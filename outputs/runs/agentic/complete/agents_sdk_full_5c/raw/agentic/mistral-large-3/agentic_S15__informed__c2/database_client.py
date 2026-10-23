import os
import boto3
from typing import Optional


def get_dynamodb_client():
    return boto3.resource(
        "dynamodb",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )


def get_table_name() -> str:
    return os.getenv("DYNAMODB_TABLE_NAME", "Documents")


def get_table():
    return get_dynamodb_client().Table(get_table_name())