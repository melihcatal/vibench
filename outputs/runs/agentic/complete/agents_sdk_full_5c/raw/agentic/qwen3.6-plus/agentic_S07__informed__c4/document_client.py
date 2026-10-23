"""
Local configuration and client helper utilities for OCR and Layout Extraction.
Provides shared configuration loading and document I/O helpers used across integration files.
"""

import os
import base64
from typing import Optional, Dict, Any, Union
from pathlib import Path


def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """Retrieve an environment variable with optional default."""
    return os.environ.get(key, default)


def load_image_bytes(file_path: Union[str, Path]) -> bytes:
    """Load a document image file as raw bytes."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Document image not found: {path}")
    with open(path, "rb") as f:
        return f.read()


def encode_image_base64(file_path: Union[str, Path]) -> str:
    """Load a document image and return base64-encoded string."""
    raw_bytes = load_image_bytes(file_path)
    return base64.b64encode(raw_bytes).decode("utf-8")


def load_pdf_bytes(file_path: Union[str, Path]) -> bytes:
    """Load a PDF document as raw bytes."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF document not found: {path}")
    with open(path, "rb") as f:
        return f.read()


def get_google_credentials_path() -> Optional[str]:
    """Return path to Google Application Credentials JSON file."""
    return get_env("GOOGLE_APPLICATION_CREDENTIALS")


def get_google_project_id() -> Optional[str]:
    """Return Google Cloud project ID for Document AI."""
    return get_env("GOOGLE_CLOUD_PROJECT")


def get_azure_document_intelligence_endpoint() -> Optional[str]:
    """Return Azure Document Intelligence service endpoint."""
    return get_env("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")


def get_azure_document_intelligence_key() -> Optional[str]:
    """Return Azure Document Intelligence API key."""
    return get_env("AZURE_DOCUMENT_INTELLIGENCE_KEY")


def get_aws_credentials() -> Dict[str, Optional[str]]:
    """Return AWS credential dict for Textract."""
    return {
        "aws_access_key_id": get_env("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": get_env("AWS_SECRET_ACCESS_KEY"),
        "aws_region": get_env("AWS_DEFAULT_REGION", "us-east-1"),
    }


def get_mindee_api_key() -> Optional[str]:
    """Return Mindee API key."""
    return get_env("MINDEE_API_KEY")


def get_alibaba_credentials() -> Dict[str, Optional[str]]:
    """Return Alibaba Cloud credential dict."""
    return {
        "access_key_id": get_env("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        "access_key_secret": get_env("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
        "region": get_env("ALIBABA_CLOUD_REGION", "cn-hangzhou"),
    }


def get_azure_content_safety_endpoint() -> Optional[str]:
    """Return Azure AI Content Safety endpoint."""
    return get_env("AZURE_CONTENT_SAFETY_ENDPOINT")


def get_azure_content_safety_key() -> Optional[str]:
    """Return Azure AI Content Safety key."""
    return get_env("AZURE_CONTENT_SAFETY_KEY")


def get_translate_credentials() -> Dict[str, Optional[str]]:
    """Return Google Cloud Translation credentials."""
    return {
        "project_id": get_env("GOOGLE_CLOUD_PROJECT"),
        "credentials_path": get_env("GOOGLE_APPLICATION_CREDENTIALS"),
    }


def get_openai_api_key() -> Optional[str]:
    """Return OpenAI API key for embeddings."""
    return get_env("OPENAI_API_KEY")


def build_mime_type(file_path: Union[str, Path]) -> str:
    """Infer MIME type from file extension."""
    ext = Path(file_path).suffix.lower()
    mime_map = {
        ".pdf": "application/pdf",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".tiff": "image/tiff",
        ".tif": "image/tiff",
        ".bmp": "image/bmp",
        ".gif": "image/gif",
    }
    return mime_map.get(ext, "application/octet-stream")
