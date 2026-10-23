import boto3
import os
from typing import Optional

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


def get_dynamodb_client(region: Optional[str] = None):
    region = region or AWS_REGION
    return boto3.client("dynamodb", region_name=region)


def get_dynamodb_resource(region: Optional[str] = None):
    region = region or AWS_REGION
    return boto3.resource("dynamodb", region_name=region)


def get_table(table_name: str, region: Optional[str] = None):
    dynamodb = get_dynamodb_resource(region)
    return dynamodb.Table(table_name)
