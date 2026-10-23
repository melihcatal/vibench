"""
Document client helper for OCR and Layout Extraction using AWS Textract.

Provides local configuration and client helper utilities for interacting
with AWS Textract API for document analysis, text extraction, and layout parsing.
"""

import os
import base64
from typing import Optional, Tuple
import boto3
from botocore.config import Config


# AWS Textract configuration constants
AWS_TEXTRACT_REGION = os.environ.get("AWS_TEXTRACT_REGION", "us-east-1")
AWS_TEXTRACT_ENDPOINT = os.environ.get("AWS_TEXTRACT_ENDPOINT", f"https://textract.{AWS_TEXTRACT_REGION}.amazonaws.com")


def get_textract_client() -> boto3.client:
    """
    Create and configure an AWS Textract client.
    
    Returns:
        boto3.client: Configured Textract client instance.
    """
    config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
        read_timeout=60,
        connect_timeout=10,
    )
    
    session = boto3.Session(
        region_name=AWS_TEXTRACT_REGION,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    
    client = session.client(
        "textract",
        config=config,
        endpoint_url=AWS_TEXTRACT_ENDPOINT if os.environ.get("AWS_TEXTRACT_ENDPOINT") else None,
    )
    return client


def load_image_as_bytes(image_path: str) -> bytes:
    """
    Load an image file from disk as raw bytes.
    
    Args:
        image_path: Path to the image file (PNG, JPEG, TIFF, PDF).
        
    Returns:
        bytes: Raw image bytes.
    """
    with open(image_path, "rb") as f:
        return f.read()


def encode_image_to_base64(image_bytes: bytes) -> str:
    """
    Encode image bytes to base64 string.
    
    Args:
        image_bytes: Raw image bytes.
        
    Returns:
        str: Base64-encoded image string.
    """
    return base64.b64encode(image_bytes).decode("utf-8")


def prepare_textract_document(image_bytes: bytes) -> dict:
    """
    Prepare a document payload for AWS Textract API.
    
    Args:
        image_bytes: Raw image bytes.
        
    Returns:
        dict: Textract-compatible document payload.
    """
    return {"Bytes": image_bytes}


def prepare_textract_document_from_path(image_path: str) -> dict:
    """
    Prepare a document payload for AWS Textract API from a file path.
    
    Args:
        image_path: Path to the image file.
        
    Returns:
        dict: Textract-compatible document payload.
    """
    image_bytes = load_image_as_bytes(image_path)
    return prepare_textract_document(image_bytes)


def validate_image_size(image_bytes: bytes, max_mb: int = 5) -> bool:
    """
    Validate that the image size is within Textract limits.
    
    Args:
        image_bytes: Raw image bytes.
        max_mb: Maximum size in megabytes (Textract limit is 5MB for sync API).
        
    Returns:
        bool: True if image size is valid.
    """
    return len(image_bytes) <= max_mb * 1024 * 1024


def get_supported_textract_features() -> list:
    """
    Return list of supported Textract feature types.
    
    Returns:
        list: List of Textract feature type strings.
    """
    return [
        "TABLES",
        "FORMS",
        "LAYOUT",
        "SIGNATURES",
    ]


class TextractConfig:
    """Configuration container for AWS Textract operations."""
    
    def __init__(
        self,
        region: str = AWS_TEXTRACT_REGION,
        timeout: int = 60,
        max_retries: int = 3,
    ):
        self.region = region
        self.timeout = timeout
        self.max_retries = max_retries
        self.endpoint_url = f"https://textract.{region}.amazonaws.com"
    
    def to_boto_config(self) -> Config:
        """Convert to botocore Config object."""
        return Config(
            retries={"max_attempts": self.max_retries, "mode": "standard"},
            read_timeout=self.timeout,
            connect_timeout=10,
        )
