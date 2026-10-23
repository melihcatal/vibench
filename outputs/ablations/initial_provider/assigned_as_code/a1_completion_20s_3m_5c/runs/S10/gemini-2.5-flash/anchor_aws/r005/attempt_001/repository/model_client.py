import boto3
import os


def get_bedrock_client():
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    client = boto3.client("bedrock-runtime", region_name=aws_region)
    return client
