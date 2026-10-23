"""
Local configuration and client helper utilities for Static Image and Visual Understanding.
Manages provider-specific client initialization and shared image processing utilities.
"""

import base64
import io
import os
from typing import Optional, Tuple, BinaryIO

import boto3
from google.cloud import vision as gc_vision
from openai import OpenAI
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def load_aws_config() -> dict:
    """Load AWS configuration from environment variables."""
    return {
        "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID", ""),
        "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
        "region_name": os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
    }


def load_google_config() -> dict:
    """Load Google Cloud configuration from environment variables."""
    return {
        "credentials_path": os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", ""),
        "project_id": os.environ.get("GOOGLE_CLOUD_PROJECT", ""),
    }


def load_openai_config() -> dict:
    """Load OpenAI configuration from environment variables."""
    return {
        "api_key": os.environ.get("OPENAI_API_KEY", ""),
        "base_url": os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    }


def load_azure_config() -> dict:
    """Load Azure configuration from environment variables."""
    return {
        "endpoint": os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", ""),
        "key": os.environ.get("AZURE_CONTENT_SAFETY_KEY", ""),
    }


def get_rekognition_client() -> boto3.client:
    """Initialize and return an AWS Rekognition client."""
    config = load_aws_config()
    return boto3.client(
        "rekognition",
        aws_access_key_id=config["aws_access_key_id"],
        aws_secret_access_key=config["aws_secret_access_key"],
        region_name=config["region_name"],
    )


def get_openai_client() -> OpenAI:
    """Initialize and return an OpenAI client."""
    config = load_openai_config()
    return OpenAI(
        api_key=config["api_key"],
        base_url=config["base_url"],
    )


def get_google_vision_client() -> gc_vision.ImageAnnotatorClient:
    """Initialize and return a Google Cloud Vision client."""
    return gc_vision.ImageAnnotatorClient()


def get_azure_content_safety_client() -> ContentSafetyClient:
    """Initialize and return an Azure Content Safety client."""
    config = load_azure_config()
    credential = AzureKeyCredential(config["key"])
    return ContentSafetyClient(
        endpoint=config["endpoint"],
        credential=credential,
    )


def encode_image_to_base64(image_data: bytes) -> str:
    """Encode raw image bytes to base64 string."""
    return base64.b64encode(image_data).decode("utf-8")


def encode_image_to_base64_url(image_data: bytes, mime_type: str = "image/jpeg") -> str:
    """Encode raw image bytes to base64 data URL."""
    b64 = encode_image_to_base64(image_data)
    return f"data:{mime_type};base64,{b64}"


def load_image_bytes(image_path: Optional[str] = None, image_bytes: Optional[bytes] = None) -> bytes:
    """Load image bytes from file path or raw bytes."""
    if image_bytes is not None:
        return image_bytes
    if image_path is not None:
        with open(image_path, "rb") as f:
            return f.read()
    raise ValueError("Either image_path or image_bytes must be provided")


def get_mime_type(image_path: str) -> str:
    """Determine MIME type from file extension."""
    ext = os.path.splitext(image_path)[1].lower()
    mime_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    return mime_map.get(ext, "image/jpeg")


class VisionProviderClients:
    """Container for all provider-specific vision clients."""

    def __init__(self):
        self._rekognition = None
        self._openai = None
        self._google_vision = None
        self._azure_safety = None

    @property
    def rekognition(self) -> boto3.client:
        if self._rekognition is None:
            self._rekognition = get_rekognition_client()
        return self._rekognition

    @property
    def openai(self) -> OpenAI:
        if self._openai is None:
            self._openai = get_openai_client()
        return self._openai

    @property
    def google_vision(self) -> gc_vision.ImageAnnotatorClient:
        if self._google_vision is None:
            self._google_vision = get_google_vision_client()
        return self._google_vision

    @property
    def azure_safety(self) -> ContentSafetyClient:
        if self._azure_safety is None:
            self._azure_safety = get_azure_content_safety_client()
        return self._azure_safety
