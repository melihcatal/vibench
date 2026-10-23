import os
import boto3

def get_s3_client():
    """
    Returns a configured boto3 S3 client.
    """
    # AWS credentials and region are typically configured via environment variables
    # or AWS CLI configuration (~/.aws/credentials, ~/.aws/config).
    # For explicit configuration, uncomment and modify the lines below.
    
    # aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    # aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    # aws_region = os.environ.get("AWS_REGION", "us-east-1")

    # if aws_access_key_id and aws_secret_access_key:
    #     s3_client = boto3.client(
    #         's3',
    #         aws_access_key_id=aws_access_key_id,
    #         aws_secret_access_key=aws_secret_access_key,
    #         region_name=aws_region
    #     )
    # else:
    #     # Rely on default credential chain (e.g., IAM role, environment variables, shared config)
    #     s3_client = boto3.client('s3', region_name=aws_region)
    
    # For this example, we'll rely on the default credential chain.
    # Ensure AWS_REGION environment variable is set or configure a default here.
    aws_region = os.environ.get("AWS_REGION", "us-east-1") # AWS_REGION signal
    return boto3.client('s3', region_name=aws_region)

def get_textract_client():
    """
    Returns a configured boto3 Textract client.
    """
    aws_region = os.environ.get("AWS_REGION", "us-east-1") # AWS_REGION signal
    return boto3.client('textract', region_name=aws_region)

def get_translate_client():
    """
    Returns a configured boto3 Translate client.
    """
    aws_region = os.environ.get("AWS_REGION", "us-east-1") # AWS_REGION signal
    return boto3.client('translate', region_name=aws_region)

def get_bedrock_runtime_client():
    """
    Returns a configured boto3 Bedrock Runtime client.
    """
    aws_region = os.environ.get("AWS_REGION", "us-east-1") # AWS_REGION signal
    return boto3.client('bedrock-runtime', region_name=aws_region)
