import os
import base64
from typing import Optional, Dict, Any
import boto3
from botocore.config import Config


AWS_REGION = os.environ.get(
    "AWS_DEFAULT_REGION", os.environ.get("AWS_REGION", "us-east-1")
)
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_SESSION_TOKEN = os.environ.get("AWS_SESSION_TOKEN", "")

REKOGNITION_ENDPOINT = os.environ.get("AWS_REKOGNITION_ENDPOINT", None)
REKOGNITION_MAX_RETRIES = int(os.environ.get("AWS_REKOGNITION_MAX_RETRIES", "3"))
REKOGNITION_TIMEOUT = int(os.environ.get("AWS_REKOGNITION_TIMEOUT", "30"))

_rekognition_client = None


def get_rekognition_client() -> boto3.client:
    global _rekognition_client

    if _rekognition_client is not None:
        return _rekognition_client

    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_session_token=AWS_SESSION_TOKEN,
        region_name=AWS_REGION,
    )

    config = Config(
        retries={"max_attempts": REKOGNITION_MAX_RETRIES, "mode": "adaptive"},
        read_timeout=REKOGNITION_TIMEOUT,
        connect_timeout=REKOGNITION_TIMEOUT,
    )

    kwargs = {"config": config}
    if REKOGNITION_ENDPOINT:
        kwargs["endpoint_url"] = REKOGNITION_ENDPOINT

    _rekognition_client = session.client("rekognition", **kwargs)
    return _rekognition_client


def load_image_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()


def image_bytes_to_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")


def validate_image_size(image_bytes: bytes, max_size_mb: float = 15.0) -> bool:
    max_bytes = int(max_size_mb * 1024 * 1024)
    return len(image_bytes) <= max_bytes


def get_provider_info() -> Dict[str, Any]:
    return {
        "provider": "aws",
        "service": "rekognition",
        "region": AWS_REGION,
        "endpoint": REKOGNITION_ENDPOINT or "rekognition.amazonaws.com",
        "model_family": "aws-rekognition-v3",
    }
