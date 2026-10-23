import os
import boto3
from botocore.config import Config

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL", "")

DEFAULT_BUCKET = os.environ.get("S3_DEFAULT_BUCKET", "")
PRESIGNED_URL_EXPIRY = int(os.environ.get("PRESIGNED_URL_EXPIRY", "3600"))


def get_s3_client():
    config_kwargs = {
        "region_name": AWS_DEFAULT_REGION,
        "config": Config(
            signature_version="s3v4",
            retries={"max_attempts": 3, "mode": "standard"},
        ),
    }
    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        config_kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
        config_kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY
    if S3_ENDPOINT_URL:
        config_kwargs["endpoint_url"] = S3_ENDPOINT_URL
    return boto3.client("s3", **config_kwargs)


def get_s3_resource():
    config_kwargs = {
        "region_name": AWS_DEFAULT_REGION,
    }
    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        config_kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
        config_kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY
    if S3_ENDPOINT_URL:
        config_kwargs["endpoint_url"] = S3_ENDPOINT_URL
    return boto3.resource("s3", **config_kwargs)


def get_textract_client():
    config_kwargs = {"region_name": AWS_DEFAULT_REGION}
    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        config_kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
        config_kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY
    return boto3.client("textract", **config_kwargs)


def get_translate_client():
    config_kwargs = {"region_name": AWS_DEFAULT_REGION}
    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        config_kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
        config_kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY
    return boto3.client("translate", **config_kwargs)


def get_bedrock_runtime_client():
    config_kwargs = {"region_name": AWS_DEFAULT_REGION}
    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        config_kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
        config_kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY
    return boto3.client("bedrock-runtime", **config_kwargs)


def validate_bucket_name(bucket):
    if not bucket:
        raise ValueError("Bucket name is required")
    if len(bucket) < 3 or len(bucket) > 63:
        raise ValueError("Bucket name must be between 3 and 63 characters")
    return bucket


def build_object_key(prefix, filename):
    prefix = prefix.rstrip("/") if prefix else ""
    if prefix:
        return f"{prefix}/{filename}"
    return filename
