import os
import boto3

def get_sqs_client():
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("sqs", region_name=aws_region)

def get_dynamodb_client():
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("dynamodb", region_name=aws_region)
