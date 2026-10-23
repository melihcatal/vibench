"""
vision_client.py - Local configuration and client helper utilities
for Static Image and Visual Understanding using AWS Rekognition.
"""

import os
import base64
import boto3
from botocore.config import Config
from typing import Optional


AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

REKOGNITION_ENDPOINT = f"https://rekognition.{AWS_REGION}.amazonaws.com"


def get_rekognition_client() -> boto3.client:
    """Create and return a configured AWS Rekognition client."""
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )
    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        connect_timeout=10,
        read_timeout=30,
    )
    return session.client("rekognition", config=config)


def load_image_as_bytes(image_path: str) -> bytes:
    """Load a local image file and return its raw bytes."""
    with open(image_path, "rb") as f:
        return f.read()


def load_image_as_base64(image_path: str) -> str:
    """Load a local image file and return base64-encoded string."""
    image_bytes = load_image_as_bytes(image_path)
    return base64.b64encode(image_bytes).decode("utf-8")


def prepare_rekognition_image_payload(image_bytes: bytes) -> dict:
    """Prepare the Image payload format expected by AWS Rekognition APIs."""
    return {"Bytes": image_bytes}


def validate_image_size(image_bytes: bytes, max_bytes: int = 5_242_880) -> bool:
    """Validate that the image is within AWS Rekognition size limits (5MB)."""
    return len(image_bytes) <= max_bytes
