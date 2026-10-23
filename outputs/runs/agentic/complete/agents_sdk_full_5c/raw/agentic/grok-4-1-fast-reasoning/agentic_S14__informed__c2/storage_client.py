import os
import boto3

STORAGE_BUCKET = os.getenv("STORAGE_BUCKET", "example-bucket")

def get_s3_client():
    return boto3.client("s3")

def get_bucket_name():
    return STORAGE_BUCKET
