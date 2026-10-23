import os
import boto3
from typing import Optional


def get_kms_client():
    """Get AWS KMS client using environment variables."""
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS credentials not found in environment variables")

    return boto3.client(
        "kms",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )


def get_openai_client():
    """Get OpenAI client for later-step integrations."""
    import openai

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    return openai.OpenAI(api_key=api_key)


def get_perspective_client():
    """Get Perspective API client for content safety."""
    import requests

    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY not found in environment variables")

    return api_key


def get_deepl_client():
    """Get DeepL client for translation."""
    import deepl

    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY not found in environment variables")

    return deepl.Translator(auth_key)
