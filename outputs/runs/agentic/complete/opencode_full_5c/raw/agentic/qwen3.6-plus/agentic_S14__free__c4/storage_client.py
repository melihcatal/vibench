import os
import boto3
from botocore.config import Config
from typing import Optional


AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL", None)
AWS_SESSION_TOKEN = os.environ.get("AWS_SESSION_TOKEN", None)

S3_TRANSFER_CONFIG = {
    "multipart_threshold": 8 * 1024 * 1024,
    "multipart_chunksize": 8 * 1024 * 1024,
    "max_concurrency": 10,
}

BOTOCORE_CONFIG = Config(
    retries={"max_attempts": 3, "mode": "standard"},
    signature_version="s3v4",
    connect_timeout=5,
    read_timeout=30,
)


def get_s3_client(region: Optional[str] = None, endpoint_url: Optional[str] = None):
    region_name = region or AWS_DEFAULT_REGION
    ep_url = endpoint_url or AWS_S3_ENDPOINT_URL

    session_kwargs = {
        "aws_access_key_id": AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
        "region_name": region_name,
    }

    if AWS_SESSION_TOKEN:
        session_kwargs["aws_session_token"] = AWS_SESSION_TOKEN

    session = boto3.Session(**session_kwargs)

    client_kwargs = {
        "config": BOTOCORE_CONFIG,
    }

    if ep_url:
        client_kwargs["endpoint_url"] = ep_url

    s3_client = session.client("s3", **client_kwargs)
    return s3_client


def get_s3_resource(region: Optional[str] = None, endpoint_url: Optional[str] = None):
    region_name = region or AWS_DEFAULT_REGION
    ep_url = endpoint_url or AWS_S3_ENDPOINT_URL

    session_kwargs = {
        "aws_access_key_id": AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
        "region_name": region_name,
    }

    if AWS_SESSION_TOKEN:
        session_kwargs["aws_session_token"] = AWS_SESSION_TOKEN

    session = boto3.Session(**session_kwargs)

    resource_kwargs = {
        "config": BOTOCORE_CONFIG,
    }

    if ep_url:
        resource_kwargs["endpoint_url"] = ep_url

    s3_resource = session.resource("s3", **resource_kwargs)
    return s3_resource


def get_textract_client(region: Optional[str] = None):
    region_name = region or AWS_DEFAULT_REGION

    session_kwargs = {
        "aws_access_key_id": AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
        "region_name": region_name,
    }

    if AWS_SESSION_TOKEN:
        session_kwargs["aws_session_token"] = AWS_SESSION_TOKEN

    session = boto3.Session(**session_kwargs)
    textract_client = session.client("textract", config=BOTOCORE_CONFIG)
    return textract_client


def get_translate_client(region: Optional[str] = None):
    region_name = region or AWS_DEFAULT_REGION

    session_kwargs = {
        "aws_access_key_id": AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
        "region_name": region_name,
    }

    if AWS_SESSION_TOKEN:
        session_kwargs["aws_session_token"] = AWS_SESSION_TOKEN

    session = boto3.Session(**session_kwargs)
    translate_client = session.client("translate", config=BOTOCORE_CONFIG)
    return translate_client


def validate_bucket_name(bucket: str) -> bool:
    if not bucket:
        return False
    if len(bucket) < 3 or len(bucket) > 63:
        return False
    if bucket.startswith("xn--"):
        return False
    if bucket.endswith("-s3alias"):
        return False
    return True


def validate_object_key(key: str) -> bool:
    if not key:
        return False
    if len(key) > 1024:
        return False
    return True


def build_s3_uri(bucket: str, key: str) -> str:
    return f"s3://{bucket}/{key}"


def parse_s3_uri(uri: str):
    if not uri.startswith("s3://"):
        raise ValueError(f"Invalid S3 URI: {uri}")
    without_scheme = uri[5:]
    parts = without_scheme.split("/", 1)
    bucket = parts[0]
    key = parts[1] if len(parts) > 1 else ""
    return bucket, key


def get_object_bytes(
    s3_client, bucket: str, key: str, version_id: Optional[str] = None
) -> bytes:
    get_kwargs = {"Bucket": bucket, "Key": key}
    if version_id:
        get_kwargs["VersionId"] = version_id
    response = s3_client.get_object(**get_kwargs)
    return response["Body"].read()
