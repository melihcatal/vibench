"""Provide local configuration and client helper utilities for Structured Document Extraction."""

import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SDEConfig:
    """Configuration for Structured Document Extraction providers."""

    aws_access_key: str = field(default_factory=lambda: os.environ.get("AWS_ACCESS_KEY_ID", ""))
    aws_secret_key: str = field(default_factory=lambda: os.environ.get("AWS_SECRET_ACCESS_KEY", ""))
    aws_region: str = field(default_factory=lambda: os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))
    google_project: str = field(default_factory=lambda: os.environ.get("GOOGLE_CLOUD_PROJECT", ""))
    google_location: str = field(default_factory=lambda: os.environ.get("GOOGLE_CLOUD_LOCATION", "us"))
    document_ai_processor: str = field(default_factory=lambda: os.environ.get("DOCUMENT_AI_PROCESSOR_ID", ""))
    openai_api_key: str = field(default_factory=lambda: os.environ.get("OPENAI_API_KEY", ""))
    openai_model: str = "gpt-4o-2024-08-06"
    anthropic_api_key: str = field(default_factory=lambda: os.environ.get("ANTHROPIC_API_KEY", ""))
    pinecone_api_key: str = field(default_factory=lambda: os.environ.get("PINECONE_API_KEY", ""))
    pinecone_index_name: str = field(default_factory=lambda: os.environ.get("PINECONE_INDEX_NAME", "expense-records"))
    pinecone_environment: str = field(default_factory=lambda: os.environ.get("PINECONE_ENVIRONMENT", "us-east1-gcp"))

    @classmethod
    def from_env(cls) -> "SDEConfig":
        """Create configuration from environment variables."""
        return cls()

    def has_aws_credentials(self) -> bool:
        return bool(self.aws_access_key and self.aws_secret_key)

    def has_google_credentials(self) -> bool:
        return bool(self.google_project and self.document_ai_processor)

    def has_openai_credentials(self) -> bool:
        return bool(self.openai_api_key)

    def has_anthropic_credentials(self) -> bool:
        return bool(self.anthropic_api_key)

    def has_pinecone_credentials(self) -> bool:
        return bool(self.pinecone_api_key and self.pinecone_index_name)


def get_textract_client():
    """Create and return an AWS Textract client using environment credentials."""
    import boto3
    from botocore.exceptions import NoCredentialsError

    config = SDEConfig.from_env()
    if not config.has_aws_credentials():
        raise NoCredentialsError("AWS credentials not found in environment")

    return boto3.client(
        "textract",
        aws_access_key_id=config.aws_access_key,
        aws_secret_access_key=config.aws_secret_key,
        region_name=config.aws_region,
    )


def get_document_ai_client():
    """Create and return a Google Cloud Document AI client."""
    from google.cloud import documentai_v1
    from google.api_core.exceptions import GoogleAPIError

    config = SDEConfig.from_env()
    if not config.has_google_credentials():
        raise GoogleAPIError("Google Cloud credentials not configured")

    return documentai_v1.DocumentProcessorServiceClient()


def get_openai_client():
    """Create and return an OpenAI client."""
    import openai

    config = SDEConfig.from_env()
    if not config.has_openai_credentials():
        raise ValueError("OpenAI API key not found in environment")

    return openai.OpenAI(api_key=config.openai_api_key)


def get_anthropic_client():
    """Create and return an Anthropic client."""
    import anthropic

    config = SDEConfig.from_env()
    if not config.has_anthropic_credentials():
        raise ValueError("Anthropic API key not found in environment")

    return anthropic.Anthropic(api_key=config.anthropic_api_key)


def get_pinecone_index():
    """Create and return a Pinecone index for expense record storage."""
    from pinecone import Pinecone

    config = SDEConfig.from_env()
    if not config.has_pinecone_credentials():
        raise ValueError("Pinecone credentials not configured")

    pc = Pinecone(api_key=config.pinecone_api_key)
    return pc.Index(config.pinecone_index_name)


def build_provider_context(provider: str, config: Optional[SDEConfig] = None) -> dict:
    """Build a provider context dictionary for tracking which service is in use."""
    if config is None:
        config = SDEConfig.from_env()

    context = {
        "provider": provider,
        "region": None,
        "model": None,
        "endpoint": None,
    }

    provider_map = {
        "aws_textract": {
            "region": config.aws_region,
            "endpoint": "textract.us-east-1.amazonaws.com",
        },
        "google_document_ai": {
            "region": config.google_location,
            "endpoint": f"{config.google_location}-documentai.googleapis.com",
        },
        "openai": {
            "model": config.openai_model,
            "endpoint": "api.openai.com",
        },
        "anthropic": {
            "model": "claude-3-5-sonnet-20241022",
            "endpoint": "api.anthropic.com",
        },
    }

    if provider in provider_map:
        context.update(provider_map[provider])

    return context


def serialize_for_response(obj) -> dict:
    """Serialize objects for API response, handling dataclasses and custom types."""
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    if hasattr(obj, "__dict__"):
        result = {}
        for key, value in obj.__dict__.items():
            if hasattr(value, "to_dict"):
                result[key] = value.to_dict()
            elif isinstance(value, (list, tuple)):
                result[key] = [
                    item.to_dict() if hasattr(item, "to_dict") else item
                    for item in value
                ]
            else:
                result[key] = value
        return result
    if isinstance(obj, (list, tuple)):
        return [serialize_for_response(item) for item in obj]
    return obj


def load_document_bytes(document_path: str) -> bytes:
    """Load document bytes from a file path."""
    with open(document_path, "rb") as f:
        return f.read()


def detect_mime_type(document_path: str) -> str:
    """Detect MIME type from file extension."""
    extension = document_path.rsplit(".", 1)[-1].lower() if "." in document_path else ""
    mime_map = {
        "pdf": "application/pdf",
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "tiff": "image/tiff",
        "tif": "image/tiff",
    }
    return mime_map.get(extension, "application/octet-stream")
