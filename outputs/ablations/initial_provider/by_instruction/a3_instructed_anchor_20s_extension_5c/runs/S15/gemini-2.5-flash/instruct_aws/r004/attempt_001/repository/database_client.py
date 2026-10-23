import boto3
import os

def get_dynamodb_client():
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("dynamodb", region_name=aws_region)
