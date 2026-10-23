import os
import boto3
from botocore.config import Config


def get_s3_client(region_name=None, endpoint_url=None):
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    region = region_name or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    config = Config(
        signature_version="s3v4",
        retries={"max_attempts": 3, "mode": "standard"},
    )

    client_kwargs = {
        "service_name": "s3",
        "aws_access_key_id": aws_access_key_id,
        "aws_secret_access_key": aws_secret_access_key,
        "region_name": region,
        "config": config,
    }

    if endpoint_url:
        client_kwargs["endpoint_url"] = endpoint_url

    return boto3.client(**client_kwargs)


def get_s3_resource(region_name=None, endpoint_url=None):
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    region = region_name or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    resource_kwargs = {
        "service_name": "s3",
        "aws_access_key_id": aws_access_key_id,
        "aws_secret_access_key": aws_secret_access_key,
        "region_name": region,
    }

    if endpoint_url:
        resource_kwargs["endpoint_url"] = endpoint_url

    return boto3.resource(**resource_kwargs)


def get_textract_client(region_name=None):
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    region = region_name or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    return boto3.client(
        service_name="textract",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region,
    )


def get_translate_client(region_name=None):
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    region = region_name or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    return boto3.client(
        service_name="translate",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region,
    )


def get_bedrock_runtime_client(region_name=None):
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    region = region_name or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    return boto3.client(
        service_name="bedrock-runtime",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region,
    )


def validate_bucket_name(bucket_name):
    if not bucket_name:
        raise ValueError("Bucket name is required")
    if len(bucket_name) < 3 or len(bucket_name) > 63:
        raise ValueError("Bucket name must be between 3 and 63 characters")
    return bucket_name


def validate_object_key(object_key):
    if not object_key:
        raise ValueError("Object key is required")
    return object_key
