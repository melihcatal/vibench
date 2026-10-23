import os
import boto3

_s3_client = None
_textract_client = None
_translate_client = None
_bedrock_runtime_client = None

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

def get_s3_client():
    global _s3_client
    if _s3_client is None:
        # AWS S3 client using boto3
        _s3_client = boto3.client("s3", region_name=AWS_REGION)
    return _s3_client

def get_textract_client():
    global _textract_client
    if _textract_client is None:
        # AWS Textract client using boto3
        _textract_client = boto3.client("textract", region_name=AWS_REGION)
    return _textract_client

def get_translate_client():
    global _translate_client
    if _translate_client is None:
        # AWS Translate client using boto3
        _translate_client = boto3.client("translate", region_name=AWS_REGION)
    return _translate_client

def get_bedrock_runtime_client():
    global _bedrock_runtime_client
    if _bedrock_runtime_client is None:
        # AWS Bedrock Runtime client using boto3
        _bedrock_runtime_client = boto3.client("bedrock-runtime", region_name=AWS_REGION)
    return _bedrock_runtime_client
