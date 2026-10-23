import os
import boto3

DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")


def get_dynamodb_client():
    return boto3.client(
        "dynamodb",
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
