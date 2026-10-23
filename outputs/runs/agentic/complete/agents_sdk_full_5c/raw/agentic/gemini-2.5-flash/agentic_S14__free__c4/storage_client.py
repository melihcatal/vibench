import os
import boto3

def get_s3_client():
    """
    Returns a configured boto3 S3 client.
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1") # Default region

    if not aws_access_key_id or not aws_secret_access_key:
        print("AWS credentials not found in environment variables. Using default credential chain.")
        return boto3.client("s3", region_name=aws_region)

    return boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )

def get_textract_client():
    """
    Returns a configured boto3 Textract client.
    """
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("textract", region_name=aws_region)

def get_translate_client():
    """
    Returns a configured boto3 Translate client.
    """
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("translate", region_name=aws_region)

def get_bedrock_runtime_client():
    """
    Returns a configured boto3 Bedrock Runtime client.
    """
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("bedrock-runtime", region_name=aws_region)
