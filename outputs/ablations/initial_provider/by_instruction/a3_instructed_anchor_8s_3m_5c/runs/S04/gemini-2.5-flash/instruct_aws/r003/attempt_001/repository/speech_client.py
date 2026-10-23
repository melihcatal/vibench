import boto3
import os

def get_transcribe_client():
    return boto3.client("transcribe", region_name=os.environ.get("AWS_REGION", "us-east-1"))

def get_s3_client():
    return boto3.client("s3", region_name=os.environ.get("AWS_REGION", "us-east-1"))

def get_translate_client():
    return boto3.client("translate", region_name=os.environ.get("AWS_REGION", "us-east-1"))

def get_comprehend_client():
    return boto3.client("comprehend", region_name=os.environ.get("AWS_REGION", "us-east-1"))

def get_bedrock_runtime_client():
    # Using a generic client for Bedrock, assuming an embedding model will be called
    return boto3.client("bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1"))
