import boto3

# AWS region for the S3 client
AWS_REGION = "us-east-1" 

def get_s3_client():
    """
    Returns a configured boto3 S3 client.
    """
    return boto3.client("s3", region_name=AWS_REGION)

def get_textract_client():
    """
    Returns a configured boto3 Textract client.
    """
    return boto3.client("textract", region_name=AWS_REGION)

def get_translate_client():
    """
    Returns a configured boto3 Translate client.
    """
    return boto3.client("translate", region_name=AWS_REGION)

def get_comprehend_client():
    """
    Returns a configured boto3 Comprehend client.
    """
    return boto3.client("comprehend", region_name=AWS_REGION)

def get_bedrock_runtime_client():
    """
    Returns a configured boto3 Bedrock Runtime client.
    """
    return boto3.client("bedrock-runtime", region_name=AWS_REGION)
