import boto3
import os
from typing import Optional


def get_dynamodb_client():
    """
    Returns a configured DynamoDB client.
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if aws_access_key_id and aws_secret_access_key:
        return boto3.client(
            "dynamodb",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region,
        )
    else:
        return boto3.client("dynamodb", region_name=aws_region)


def get_s3_client():
    """
    Returns a configured S3 client.
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if aws_access_key_id and aws_secret_access_key:
        return boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region,
        )
    else:
        return boto3.client("s3", region_name=aws_region)


def get_comprehend_client():
    """
    Returns a configured Amazon Comprehend client.
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if aws_access_key_id and aws_secret_access_key:
        return boto3.client(
            "comprehend",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region,
        )
    else:
        return boto3.client("comprehend", region_name=aws_region)


def get_translate_client():
    """
    Returns a configured Amazon Translate client.
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if aws_access_key_id and aws_secret_access_key:
        return boto3.client(
            "translate",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region,
        )
    else:
        return boto3.client("translate", region_name=aws_region)


def get_bedrock_client():
    """
    Returns a configured Amazon Bedrock client.
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if aws_access_key_id and aws_secret_access_key:
        return boto3.client(
            "bedrock-runtime",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region,
        )
    else:
        return boto3.client("bedrock-runtime", region_name=aws_region)
