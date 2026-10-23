import boto3
import os


def get_dynamodb_client(region_name=None):
    region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
    return boto3.resource("dynamodb", region_name=region_name)
