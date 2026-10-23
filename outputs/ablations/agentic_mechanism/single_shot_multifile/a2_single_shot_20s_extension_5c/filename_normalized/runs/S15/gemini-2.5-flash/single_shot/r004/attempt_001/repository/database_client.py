import os
import boto3

def get_dynamodb_client():
    region = os.environ.get("AWS_REGION")
    if not region:
        raise ValueError("AWS_REGION environment variable not set.")
    return boto3.client("dynamodb", region_name=region)

def get_dynamodb_table_name():
    table_name = os.environ.get("AWS_DYNAMODB_TABLE_NAME")
    if not table_name:
        raise ValueError("AWS_DYNAMODB_TABLE_NAME environment variable not set.")
    return table_name
