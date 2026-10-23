import boto3
import os

def get_s3_client():
    """
    Provides a configured boto3 S3 client.
    """
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    return s3_client

def get_textract_client():
    """
    Provides a configured boto3 Textract client.
    """
    textract_client = boto3.client(
        'textract',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    return textract_client

def get_translate_client():
    """
    Provides a configured boto3 Translate client.
    """
    translate_client = boto3.client(
        'translate',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    return translate_client

def get_bedrock_runtime_client():
    """
    Provides a configured boto3 Bedrock Runtime client.
    """
    bedrock_runtime_client = boto3.client(
        'bedrock-runtime',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    return bedrock_runtime_client

# Example of identifiable signal: AWS services are used via boto3 clients
