import os
import boto3
from botocore.exceptions import ClientError


def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    )


def get_bucket():
    bucket = os.getenv("S3_BUCKET_NAME")
    if not bucket:
        raise ValueError("S3_BUCKET_NAME environment variable is required")
    return bucket


def download_bytes(key: str) -> bytes:
    client = get_s3_client()
    bucket = get_bucket()
    response = client.get_object(Bucket=bucket, Key=key)
    return response["Body"].read()


def download_text(key: str) -> str:
    data = download_bytes(key)
    return data.decode("utf-8")
