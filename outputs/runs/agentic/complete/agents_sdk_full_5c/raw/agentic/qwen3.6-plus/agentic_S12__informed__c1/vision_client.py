"""
vision_client.py - Local configuration and client helper utilities
for Static Image and Visual Understanding via Amazon Rekognition.

Provider: Amazon Rekognition
SDK: boto3
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

import os
import base64
from typing import Optional

import boto3
from botocore.config import Config


def get_rekognition_client(region_name: Optional[str] = None):
    """
    Create and return an Amazon Rekognition client using boto3.

    Uses environment variables:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_DEFAULT_REGION (optional, falls back to region_name or us-east-1)
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    region = region_name or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables "
            "must be set for Amazon Rekognition access."
        )

    config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
        read_timeout=30,
        connect_timeout=10,
    )

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region,
    )

    client = session.client("rekognition", config=config)
    return client


def load_image_bytes(image_path: str) -> bytes:
    """Read an image file from disk and return its raw bytes."""
    with open(image_path, "rb") as f:
        return f.read()


def encode_image_to_base64(image_path: str) -> str:
    """Read an image file and return a base64-encoded string."""
    image_bytes = load_image_bytes(image_path)
    return base64.b64encode(image_bytes).decode("utf-8")


def get_rekognition_image_payload(image_path: Optional[str] = None, image_bytes: Optional[bytes] = None):
    """
    Build the Image payload dict for Amazon Rekognition API calls.

    Accepts either an image_path (str) or raw image_bytes.
    Returns a dict suitable for the Image parameter in Rekognition calls.
    """
    if image_path is not None:
        raw_bytes = load_image_bytes(image_path)
    elif image_bytes is not None:
        raw_bytes = image_bytes
    else:
        raise ValueError("Either image_path or image_bytes must be provided.")

    return {"Bytes": raw_bytes}
