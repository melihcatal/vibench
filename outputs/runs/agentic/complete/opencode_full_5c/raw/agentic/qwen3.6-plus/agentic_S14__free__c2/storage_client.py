import os
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


AWS_S3_ENDPOINT = "https://s3.amazonaws.com"
DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN", "")


def get_s3_client(region_name=None, endpoint_url=None):
    region = region_name or DEFAULT_REGION
    cfg = Config(
        signature_version="s3v4",
        retries={"max_attempts": 3, "mode": "standard"},
    )
    kwargs = {
        "service_name": "s3",
        "region_name": region,
        "config": cfg,
    }
    if endpoint_url:
        kwargs["endpoint_url"] = endpoint_url
    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
        kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY
    if AWS_SESSION_TOKEN:
        kwargs["aws_session_token"] = AWS_SESSION_TOKEN
    return boto3.client(**kwargs)


def get_s3_resource(region_name=None, endpoint_url=None):
    region = region_name or DEFAULT_REGION
    cfg = Config(
        signature_version="s3v4",
        retries={"max_attempts": 3, "mode": "standard"},
    )
    kwargs = {
        "service_name": "s3",
        "region_name": region,
        "config": cfg,
    }
    if endpoint_url:
        kwargs["endpoint_url"] = endpoint_url
    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
        kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY
    if AWS_SESSION_TOKEN:
        kwargs["aws_session_token"] = AWS_SESSION_TOKEN
    return boto3.resource(**kwargs)


def get_textract_client(region_name=None):
    region = region_name or DEFAULT_REGION
    kwargs = {
        "service_name": "textract",
        "region_name": region,
    }
    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
        kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY
    if AWS_SESSION_TOKEN:
        kwargs["aws_session_token"] = AWS_SESSION_TOKEN
    return boto3.client(**kwargs)


def get_translate_client(region_name=None):
    region = region_name or DEFAULT_REGION
    kwargs = {
        "service_name": "translate",
        "region_name": region,
    }
    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
        kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY
    if AWS_SESSION_TOKEN:
        kwargs["aws_session_token"] = AWS_SESSION_TOKEN
    return boto3.client(**kwargs)


def get_bedrock_runtime_client(region_name=None):
    region = region_name or DEFAULT_REGION
    kwargs = {
        "service_name": "bedrock-runtime",
        "region_name": region,
    }
    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
        kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY
    if AWS_SESSION_TOKEN:
        kwargs["aws_session_token"] = AWS_SESSION_TOKEN
    return boto3.client(**kwargs)


def validate_bucket_name(bucket):
    if not bucket or not isinstance(bucket, str):
        raise ValueError("Bucket name must be a non-empty string")
    if len(bucket) < 3 or len(bucket) > 63:
        raise ValueError("Bucket name must be between 3 and 63 characters")
    return bucket


def build_object_key(prefix, filename):
    if prefix and not prefix.endswith("/"):
        prefix = prefix + "/"
    return f"{prefix}{filename}" if prefix else filename


def handle_s3_error(exc, operation, bucket, key=None):
    error_code = exc.response.get("Error", {}).get("Code", "Unknown")
    error_message = exc.response.get("Error", {}).get("Message", str(exc))
    detail = f"Bucket: {bucket}"
    if key:
        detail += f", Key: {key}"
    raise RuntimeError(
        f"S3 {operation} failed [{error_code}]: {error_message} ({detail})"
    ) from exc
