import boto3
import os

def get_textract_client():
    """
    Returns an AWS Textract client.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("textract", region_name=region_name)

def get_comprehend_client():
    """
    Returns an AWS Comprehend client.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("comprehend", region_name=region_name)

def get_dynamodb_client():
    """
    Returns an AWS DynamoDB client.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("dynamodb", region_name=region_name)
