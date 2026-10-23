import os
import boto3
from botocore.config import Config


def get_s3_client():
    """
    Create and return an S3 client with configuration from environment variables.

    Returns:
        boto3 S3 client instance
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError(
            "AWS credentials not found in environment variables. "
            "Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY."
        )

    config = Config(retries={"max_attempts": 3, "mode": "standard"})

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )

    return session.client("s3", config=config)


def get_textract_client():
    """
    Create and return a Textract client for OCR operations.

    Returns:
        boto3 Textract client instance
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError(
            "AWS credentials not found in environment variables. "
            "Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY."
        )

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )

    return session.client("textract")


def get_translate_client():
    """
    Create and return a Translate client for translation operations.

    Returns:
        boto3 Translate client instance
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError(
            "AWS credentials not found in environment variables. "
            "Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY."
        )

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )

    return session.client("translate")


def get_bedrock_client():
    """
    Create and return a Bedrock Runtime client for LLM operations.

    Returns:
        boto3 Bedrock Runtime client instance
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError(
            "AWS credentials not found in environment variables. "
            "Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY."
        )

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )

    return session.client("bedrock-runtime")
