"""
Local configuration and client helper utilities for Structured Document Extraction.

Provides configuration loading, client initialization helpers, and shared utilities
used across the document extraction service integrations.
"""

import os
import json
import base64
from typing import Optional, Dict, Any, Tuple
from dataclasses import dataclass, field


@dataclass
class ProviderConfig:
    """Configuration for a document extraction provider."""
    provider_name: str
    api_key: str = ""
    api_secret: str = ""
    endpoint: str = ""
    region: str = ""
    model_id: str = ""
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentExtractionConfig:
    """Aggregated configuration for document extraction services."""
    aws: ProviderConfig = field(default_factory=lambda: ProviderConfig(
        provider_name="aws-textract",
        region=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
    ))
    azure: ProviderConfig = field(default_factory=lambda: ProviderConfig(
        provider_name="azure-document-intelligence",
        endpoint=os.environ.get(
            "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
            "https://default-resource.cognitiveservices.azure.com/",
        ),
        api_key=os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_API_KEY", ""),
        model_id="prebuilt-receipt",
    ))
    google: ProviderConfig = field(default_factory=lambda: ProviderConfig(
        provider_name="google-document-ai",
        region=os.environ.get("GOOGLE_CLOUD_LOCATION", "us"),
        model_id=os.environ.get("DOCUMENT_AI_PROCESSOR_ID", "expense-processor"),
    ))
    bedrock: ProviderConfig = field(default_factory=lambda: ProviderConfig(
        provider_name="aws-bedrock",
        region=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    ))
    pinecone: ProviderConfig = field(default_factory=lambda: ProviderConfig(
        provider_name="pinecone",
        api_key=os.environ.get("PINECONE_API_KEY", ""),
        endpoint=os.environ.get("PINECONE_ENVIRONMENT", ""),
        extra={
            "index_name": os.environ.get("PINECONE_INDEX_NAME", "expense-records"),
        },
    ))


def load_config(config_path: Optional[str] = None) -> DocumentExtractionConfig:
    """
    Load document extraction configuration from environment variables and optional config file.
    
    Args:
        config_path: Optional path to JSON configuration file
    
    Returns:
        DocumentExtractionConfig with merged settings
    """
    config = DocumentExtractionConfig()
    
    if config_path and os.path.exists(config_path):
        with open(config_path, "r") as f:
            file_config = json.load(f)
        config = _merge_file_config(config, file_config)
    
    return config


def _merge_file_config(
    config: DocumentExtractionConfig,
    file_config: Dict[str, Any],
) -> DocumentExtractionConfig:
    """Merge file-based configuration into existing config."""
    if "aws" in file_config:
        aws_cfg = file_config["aws"]
        config.aws.region = aws_cfg.get("region", config.aws.region)
        config.aws.api_key = aws_cfg.get("api_key", config.aws.api_key)
        config.aws.api_secret = aws_cfg.get("api_secret", config.aws.api_secret)
    
    if "azure" in file_config:
        azure_cfg = file_config["azure"]
        config.azure.endpoint = azure_cfg.get("endpoint", config.azure.endpoint)
        config.azure.api_key = azure_cfg.get("api_key", config.azure.api_key)
        config.azure.model_id = azure_cfg.get("model_id", config.azure.model_id)
    
    if "google" in file_config:
        google_cfg = file_config["google"]
        config.google.region = google_cfg.get("region", config.google.region)
        config.google.model_id = google_cfg.get("model_id", config.google.model_id)
    
    if "bedrock" in file_config:
        bedrock_cfg = file_config["bedrock"]
        config.bedrock.region = bedrock_cfg.get("region", config.bedrock.region)
        config.bedrock.model_id = bedrock_cfg.get("model_id", config.bedrock.model_id)
    
    if "pinecone" in file_config:
        pinecone_cfg = file_config["pinecone"]
        config.pinecone.api_key = pinecone_cfg.get("api_key", config.pinecone.api_key)
        config.pinecone.extra["index_name"] = pinecone_cfg.get(
            "index_name",
            config.pinecone.extra.get("index_name", "expense-records"),
        )
    
    return config


def encode_document_for_api(document_path: Optional[str] = None, document_bytes: Optional[bytes] = None) -> Tuple[bytes, str]:
    """
    Encode a document for API transmission.
    
    Args:
        document_path: Path to document file
        document_bytes: Raw document bytes
    
    Returns:
        Tuple of (raw_bytes, mime_type)
    """
    if document_bytes:
        return document_bytes, _detect_mime_type(document_bytes)
    
    if document_path:
        with open(document_path, "rb") as f:
            raw_bytes = f.read()
        return raw_bytes, _detect_mime_type(raw_bytes, document_path)
    
    raise ValueError("Either document_path or document_bytes must be provided")


def _detect_mime_type(raw_bytes: bytes, file_path: Optional[str] = None) -> str:
    """Detect MIME type from file bytes or extension."""
    if raw_bytes[:4] == b"%PDF":
        return "application/pdf"
    if raw_bytes[:8] == b"\x89PNG\r\n\x1a\n":
        return "image/png"
    if raw_bytes[:2] in (b"\xff\xd8", b"\xff\xd9"):
        return "image/jpeg"
    if raw_bytes[:4] in (b"II\x2a\x00", b"MM\x00\x2a"):
        return "image/tiff"
    
    if file_path:
        ext = os.path.splitext(file_path)[1].lower()
        mime_map = {
            ".pdf": "application/pdf",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".tiff": "image/tiff",
            ".tif": "image/tiff",
        }
        return mime_map.get(ext, "application/octet-stream")
    
    return "application/octet-stream"


def build_confidence_threshold_check(
    min_confidence: float = 0.70,
    required_fields: Optional[list] = None,
) -> Dict[str, Any]:
    """
    Build a confidence threshold validation configuration.
    
    Args:
        min_confidence: Minimum acceptable confidence score
        required_fields: Fields that must pass confidence check
    
    Returns:
        Configuration dictionary for validation
    """
    fields = required_fields or ["vendor", "date", "total_amount"]
    return {
        "min_confidence": min_confidence,
        "required_fields": fields,
        "field_overrides": {
            "line_items": 0.50,
            "tax_amount": 0.60,
        },
    }


def format_extraction_result_as_json(extracted_data: Dict[str, Any], indent: int = 2) -> str:
    """Format extraction result dictionary as JSON string."""
    return json.dumps(extracted_data, indent=indent, default=str)


def sanitize_field_value(value: Any) -> Any:
    """Sanitize a field value for safe storage and transmission."""
    if value is None:
        return None
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, (list, dict)):
        return value
    return str(value)
