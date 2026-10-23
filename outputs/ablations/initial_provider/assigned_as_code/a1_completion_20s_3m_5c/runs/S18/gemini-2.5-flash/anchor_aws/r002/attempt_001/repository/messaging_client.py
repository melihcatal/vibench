import boto3
import os

def get_sns_client(region_name=None):
    region = region_name or os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("sns", region_name=region)

def get_sqs_client(region_name=None):
    region = region_name or os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("sqs", region_name=region)

def get_comprehend_client(region_name=None):
    region = region_name or os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("comprehend", region_name=region)

def get_translate_client(region_name=None):
    region = region_name or os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("translate", region_name=region)

def get_dynamodb_client(region_name=None):
    region = region_name or os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("dynamodb", region_name=region)

def get_cloudwatch_logs_client(region_name=None):
    region = region_name or os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("logs", region_name=region)
