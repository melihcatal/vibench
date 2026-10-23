import os

import boto3


def get_dynamodb_client():
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("dynamodb", region_name=region_name)


def get_dynamodb_resource():
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.resource("dynamodb", region_name=region_name)
