import os
import boto3

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

def get_s3_client():
    if not S3_BUCKET_NAME:
        raise ValueError("S3_BUCKET_NAME environment variable not set")
    return boto3.client("s3", region_name=AWS_REGION)

def get_textract_client():
    return boto3.client("textract", region_name=AWS_REGION)

def get_translate_client():
    return boto3.client("translate", region_name=AWS_REGION)
