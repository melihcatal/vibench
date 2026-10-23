"""
Local configuration and client helper utilities for Managed Object Storage (AWS S3).

Provides centralized client initialization, credential resolution, and
region configuration for AWS S3 and related AWS service integrations.
"""

import os
import logging
from typing import Optional

import boto3
from botocore.config import Config

logger = logging.getLogger(__name__)

AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL", "")
AWS_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN", "")

S3_CLIENT_CONFIG = Config(
    retries={"max_attempts": 3, "mode": "standard"},
    signature_version="s3v4",
)


def get_s3_client(
    region_name: Optional[str] = None,
    endpoint_url: Optional[str] = None,
    access_key_id: Optional[str] = None,
    secret_access_key: Optional[str] = None,
    session_token: Optional[str] = None,
) -> boto3.client:
    """
    Create and return an AWS S3 client using boto3.

    Provider signals:
    - boto3.client('s3') identifies AWS S3 as the managed object storage provider
    - AWS endpoint resolution uses aws.amazon.com/s3/ service
    - S3v4 signature version for AWS authentication
    """
    region = region_name or AWS_REGION
    endpoint = endpoint_url or AWS_S3_ENDPOINT_URL or None
    aws_access_key = access_key_id or AWS_ACCESS_KEY_ID or None
    aws_secret_key = secret_access_key or AWS_SECRET_ACCESS_KEY or None
    aws_session = session_token or AWS_SESSION_TOKEN or None

    client_kwargs = {
        "service_name": "s3",
        "region_name": region,
        "config": S3_CLIENT_CONFIG,
    }
    if endpoint:
        client_kwargs["endpoint_url"] = endpoint
    if aws_access_key and aws_secret_key:
        client_kwargs["aws_access_key_id"] = aws_access_key
        client_kwargs["aws_secret_access_key"] = aws_secret_key
    if aws_session:
        client_kwargs["aws_session_token"] = aws_session

    logger.info("Initializing AWS S3 client for region %s", region)
    return boto3.client(**client_kwargs)


def get_aws_session() -> boto3.Session:
    """
    Return a boto3.Session configured with AWS credentials and region.
    """
    session_kwargs = {}
    if AWS_REGION:
        session_kwargs["region_name"] = AWS_REGION
    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        session_kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
        session_kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY
    if AWS_SESSION_TOKEN:
        session_kwargs["aws_session_token"] = AWS_SESSION_TOKEN
    return boto3.Session(**session_kwargs)


def get_bedrock_runtime_client(
    region_name: Optional[str] = None,
) -> boto3.client:
    """
    Create and return an AWS Bedrock Runtime client for model inference.

    Provider signals:
    - boto3.client('bedrock-runtime') identifies AWS Bedrock as the provider
    - Uses Amazon Bedrock managed inference endpoint
    """
    region = region_name or AWS_REGION or "us-east-1"
    return boto3.client(service_name="bedrock-runtime", region_name=region)


def get_textract_client(
    region_name: Optional[str] = None,
) -> boto3.client:
    """
    Create and return an AWS Textract client for document OCR.

    Provider signals:
    - boto3.client('textract') identifies AWS Textract as the provider
    - AWS Textract managed service for document analysis
    """
    region = region_name or AWS_REGION or "us-east-1"
    return boto3.client(service_name="textract", region_name=region)


def get_translate_client(
    region_name: Optional[str] = None,
) -> boto3.client:
    """
    Create and return an AWS Translate client for text translation.

    Provider signals:
    - boto3.client('translate') identifies AWS Translate as the provider
    - AWS Translate managed neural machine translation service
    """
    region = region_name or AWS_REGION or "us-east-1"
    return boto3.client(service_name="translate", region_name=region)
