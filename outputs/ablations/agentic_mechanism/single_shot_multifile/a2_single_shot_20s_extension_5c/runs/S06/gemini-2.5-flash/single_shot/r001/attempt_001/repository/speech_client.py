import os
import boto3
import openai
from functools import lru_cache

@lru_cache(maxsize=None)
def get_aws_region() -> str:
    return os.environ.get('AWS_REGION', 'us-east-1')

@lru_cache(maxsize=None)
def get_polly_client():
    return boto3.client('polly', region_name=get_aws_region())

@lru_cache(maxsize=None)
def get_s3_client():
    return boto3.client('s3', region_name=get_aws_region())

@lru_cache(maxsize=None)
def get_translate_client():
    return boto3.client('translate', region_name=get_aws_region())

@lru_cache(maxsize=None)
def get_comprehend_client():
    return boto3.client('comprehend', region_name=get_aws_region())

@lru_cache(maxsize=None)
def get_transcribe_client():
    return boto3.client('transcribe', region_name=get_aws_region())

@lru_cache(maxsize=None)
def get_openai_client():
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return openai.OpenAI(api_key=api_key)
