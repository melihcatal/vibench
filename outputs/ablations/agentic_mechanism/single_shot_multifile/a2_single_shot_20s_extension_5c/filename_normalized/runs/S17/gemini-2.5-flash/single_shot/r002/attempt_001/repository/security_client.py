import os
import boto3
from botocore.exceptions import ClientError
import openai

def get_aws_session():
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    if not all([aws_access_key_id, aws_secret_access_key]):
        print("AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) not found in environment variables. Using default credential chain.")
        return boto3.Session(region_name=aws_region)
    
    return boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )

def get_kms_client():
    session = get_aws_session()
    return session.client('kms')

def get_cloudtrail_client():
    session = get_aws_session()
    return session.client('cloudtrail')

def get_comprehend_client():
    session = get_aws_session()
    return session.client('comprehend')

def get_translate_client():
    session = get_aws_session()
    return session.client('translate')

def get_openai_client():
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    openai.api_key = openai_api_key
    return openai.OpenAI(api_key=openai_api_key)