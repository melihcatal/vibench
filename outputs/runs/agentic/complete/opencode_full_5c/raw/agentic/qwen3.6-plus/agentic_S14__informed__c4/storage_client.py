import os
import boto3
from botocore.config import Config


def get_s3_client():
    endpoint_url = os.environ.get("AWS_S3_ENDPOINT_URL")
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    region_name = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    config = Config(
        signature_version="s3v4",
        retries={"max_attempts": 3, "mode": "standard"},
    )

    session_kwargs = {
        "region_name": region_name,
        "config": config,
    }
    if aws_access_key_id and aws_secret_access_key:
        session_kwargs["aws_access_key_id"] = aws_access_key_id
        session_kwargs["aws_secret_access_key"] = aws_secret_access_key
    if endpoint_url:
        session_kwargs["endpoint_url"] = endpoint_url

    return boto3.client("s3", **session_kwargs)


def get_bucket_name():
    return os.environ.get("S3_BUCKET_NAME", "managed-storage-bucket")
