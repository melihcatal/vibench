import os
import boto3
from openai import OpenAI

def get_secrets_manager_client():
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("secretsmanager", region_name=region_name)

def get_comprehend_client():
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("comprehend", region_name=region_name)

def get_translate_client():
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("translate", region_name=region_name)

def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return OpenAI(api_key=api_key)
