"""
vision_client.py - Provide local configuration and client helper utilities
for Static Image and Visual Understanding.
"""

import base64
import os
from pathlib import Path
from typing import Optional, Dict, Any, Union

import requests


def load_image_bytes(image_source: Union[str, Path, bytes]) -> bytes:
    """Load image bytes from a file path or return raw bytes."""
    if isinstance(image_source, (str, Path)):
        path = Path(image_source)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {path}")
        return path.read_bytes()
    return image_source


def encode_image_base64(image_bytes: bytes) -> str:
    """Encode image bytes to a base64 string."""
    return base64.b64encode(image_bytes).decode("utf-8")


def detect_image_mime(image_bytes: bytes) -> str:
    """Detect the MIME type of an image from its header bytes."""
    if image_bytes.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if image_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if image_bytes.startswith(b"GIF87a") or image_bytes.startswith(b"GIF89a"):
        return "image/gif"
    if image_bytes.startswith(b"RIFF") and image_bytes[8:12] == b"WEBP":
        return "image/webp"
    return "application/octet-stream"


def load_env_credentials(env_var: str, default: Optional[str] = None) -> Optional[str]:
    """Load a credential value from an environment variable."""
    return os.environ.get(env_var, default)


def build_aws_session(region: Optional[str] = None):
    """Build and return a boto3 session for AWS services."""
    import boto3

    aws_region = region or load_env_credentials("AWS_DEFAULT_REGION", "us-east-1")
    return boto3.Session(region_name=aws_region)


def build_openai_client(api_key: Optional[str] = None):
    """Build and return an OpenAI API client."""
    from openai import OpenAI

    key = api_key or load_env_credentials("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=key)


def build_google_vision_client(
    credentials_path: Optional[str] = None, api_key: Optional[str] = None
):
    """Build and return a Google Cloud Vision client."""
    from google.cloud import vision_v1

    if credentials_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    return vision_v1.ImageAnnotatorClient()


def build_anthropic_client(api_key: Optional[str] = None):
    """Build and return an Anthropic API client."""
    import anthropic

    key = api_key or load_env_credentials("ANTHROPIC_API_KEY")
    if not key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")
    return anthropic.Anthropic(api_key=key)


def build_deepl_client(api_key: Optional[str] = None):
    """Build and return a DeepL translator configuration."""
    key = api_key or load_env_credentials("DEEPL_API_KEY")
    if not key:
        raise ValueError("DEEPL_API_KEY environment variable is required")
    return {"auth_key": key, "api_url": "https://api-free.deepl.com/v2/translate"}


def build_s3_client(region: Optional[str] = None):
    """Build and return an AWS S3 client."""
    session = build_aws_session(region)
    return session.client("s3")


def prepare_image_payload(image_source: Union[str, Path, bytes]) -> Dict[str, Any]:
    """Prepare a normalized image payload dictionary."""
    image_bytes = load_image_bytes(image_source)
    mime_type = detect_image_mime(image_bytes)
    base64_data = encode_image_base64(image_bytes)
    return {
        "image_bytes": image_bytes,
        "mime_type": mime_type,
        "base64_data": base64_data,
    }
