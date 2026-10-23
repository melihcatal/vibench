"""
Local configuration and client helper utilities for Static Image and Visual Understanding.

Supports Amazon Rekognition, Azure AI Vision, and general image I/O helpers.
"""

import os
import base64
import io
from typing import Optional, Dict, Any, Union
from pathlib import Path

import boto3
from botocore.config import Config


# ---------------------------------------------------------------------------
# Configuration loaders
# ---------------------------------------------------------------------------

def load_aws_config(region: Optional[str] = None) -> Dict[str, Any]:
    """Load AWS configuration for Rekognition clients."""
    aws_region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    session_kwargs = {
        "region_name": aws_region,
    }
    if aws_access_key and aws_secret_key:
        session_kwargs["aws_access_key_id"] = aws_access_key
        session_kwargs["aws_secret_access_key"] = aws_secret_key

    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        connect_timeout=10,
        read_timeout=30,
    )

    client = boto3.client("rekognition", config=config, **session_kwargs)
    return {"client": client, "region": aws_region}


def load_azure_vision_config(
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> Dict[str, str]:
    """Load Azure AI Vision configuration."""
    az_endpoint = endpoint or os.environ.get("AZURE_VISION_ENDPOINT", "")
    az_key = key or os.environ.get("AZURE_VISION_KEY", "")

    if not az_endpoint:
        raise ValueError("AZURE_VISION_ENDPOINT environment variable must be set")
    if not az_key:
        raise ValueError("AZURE_VISION_KEY environment variable must be set")

    return {
        "endpoint": az_endpoint.rstrip("/"),
        "key": az_key,
        "api_version": "2023-02-01-preview",
    }


# ---------------------------------------------------------------------------
# Image I/O helpers
# ---------------------------------------------------------------------------

def load_image_bytes(image_source: Union[str, bytes, io.BytesIO, Path]) -> bytes:
    """Load image bytes from a file path, URL string, raw bytes, or file-like object."""
    if isinstance(image_source, (bytes, io.BytesIO)):
        if isinstance(image_source, io.BytesIO):
            return image_source.getvalue()
        return image_source

    path = Path(image_source)
    if path.exists():
        return path.read_bytes()

    raise FileNotFoundError(f"Image source not found: {image_source}")


def image_bytes_to_base64(image_bytes: bytes) -> str:
    """Encode image bytes as a base64 string."""
    return base64.b64encode(image_bytes).decode("utf-8")


def get_image_format(image_bytes: bytes) -> str:
    """Detect image format from magic bytes."""
    if image_bytes.startswith(b"\xff\xd8\xff"):
        return "JPEG"
    elif image_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
        return "PNG"
    elif image_bytes.startswith(b"GIF87a") or image_bytes.startswith(b"GIF89a"):
        return "GIF"
    elif image_bytes.startswith(b"RIFF") and image_bytes[8:12] == b"WEBP":
        return "WEBP"
    return "JPEG"  # default fallback


# ---------------------------------------------------------------------------
# Rekognition-specific helpers
# ---------------------------------------------------------------------------

def build_rekognition_image_payload(image_source: Union[str, bytes, io.BytesIO, Path]) -> Dict[str, Any]:
    """Build an image payload dict suitable for Amazon Rekognition API calls."""
    image_bytes = load_image_bytes(image_source)
    return {"Bytes": image_bytes}


def create_rekognition_client(region: Optional[str] = None):
    """Create and return a boto3 Rekognition client."""
    config = load_aws_config(region)
    return config["client"]
