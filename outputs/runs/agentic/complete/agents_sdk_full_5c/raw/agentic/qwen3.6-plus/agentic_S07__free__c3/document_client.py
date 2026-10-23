"""
Local configuration and client helper utilities for OCR and Layout Extraction.
Uses AWS Textract as the concrete provider.
"""

import os
from typing import Optional

import boto3
from botocore.config import Config


# Provider-identifying: AWS Textract endpoint
TEXTRACT_ENDPOINT = os.environ.get(
    "AWS_TEXTRACT_ENDPOINT", "https://textract.us-east-1.amazonaws.com"
)

TEXTRACT_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")


def create_textract_client(
    region_name: Optional[str] = None,
    max_retries: int = 3,
    timeout: int = 30,
) -> boto3.client:
    """
    Create a boto3 Textract client with provider-specific configuration.

    Args:
        region_name: AWS region (defaults to Textract provider default)
        max_retries: Maximum retry attempts
        timeout: Request timeout in seconds

    Returns:
        Configured boto3 Textract client
    """
    config = Config(
        retries={"max_attempts": max_retries},
        connect_timeout=timeout,
        read_timeout=timeout,
    )

    session_kwargs = {}
    if AWS_ACCESS_KEY and AWS_SECRET_KEY:
        session_kwargs["aws_access_key_id"] = AWS_ACCESS_KEY
        session_kwargs["aws_secret_access_key"] = AWS_SECRET_KEY
    if region_name or Textract_REGION:
        session_kwargs["region_name"] = region_name or Textract_REGION

    client = boto3.client("textract", config=config, **session_kwargs)
    return client


def load_image_bytes(image_path: str) -> bytes:
    """
    Load image file as bytes for Textract API consumption.

    Args:
        image_path: Path to image file (PNG, JPEG, TIFF, PDF)

    Returns:
        Raw image bytes
    """
    with open(image_path, "rb") as f:
        return f.read()


def build_textract_image_payload(image_bytes: bytes) -> dict:
    """
    Build Textract-specific request payload from image bytes.

    Args:
        image_bytes: Raw image data

    Returns:
        Dictionary with Bytes key for Textract API
    """
    return {"Bytes": image_bytes}


def normalize_textract_response(raw_response: dict) -> dict:
    """
    Normalize raw Textract response into consistent structure.

    Args:
        raw_response: Raw API response from Textract

    Returns:
        Normalized response with Blocks, DocumentMetadata, and AnalyzeDocumentModelVersion
    """
    return {
        "blocks": raw_response.get("Blocks", []),
        "document_metadata": raw_response.get("DocumentMetadata", {}),
        "model_version": raw_response.get("AnalyzeDocumentModelVersion", ""),
        "status_code": raw_response.get("ResponseMetadata", {}).get("HTTPStatusCode"),
    }


def extract_page_blocks(blocks: list, page_index: int = 0) -> list:
    """
    Filter Textract blocks for a specific page.

    Args:
        blocks: List of Textract Block objects
        page_index: Zero-based page index

    Returns:
        Filtered blocks for the specified page
    """
    return [
        block for block in blocks
        if block.get("BlockType") == "PAGE" and block.get("Page") == page_index
    ]
