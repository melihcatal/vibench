"""
Local configuration and client helper utilities for Structured Document Extraction.

Provides unified client initialization, credential management, and shared
utilities for interacting with various document extraction providers.
"""

import os
from typing import Any, Dict, Optional


def load_env_var(name: str, default: Optional[str] = None) -> Optional[str]:
    """Load an environment variable with an optional default."""
    return os.environ.get(name, default)


def validate_credentials(*env_vars: str) -> None:
    """Validate that all required credential environment variables are set."""
    missing = [var for var in env_vars if not os.environ.get(var)]
    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}"
        )


class DocumentClientConfig:
    """Configuration container for document extraction clients."""

    def __init__(
        self,
        provider: str,
        credentials: Dict[str, str],
        endpoint: Optional[str] = None,
        model_id: Optional[str] = None,
    ):
        self.provider = provider
        self.credentials = credentials
        self.endpoint = endpoint
        self.model_id = model_id

    def get_credential(self, key: str) -> str:
        """Retrieve a credential by key."""
        if key not in self.credentials:
            raise KeyError(f"Missing credential key: {key}")
        return self.credentials[key]

    def to_dict(self) -> Dict[str, Any]:
        """Serialize config to dictionary."""
        return {
            "provider": self.provider,
            "endpoint": self.endpoint,
            "model_id": self.model_id,
        }


def build_azure_di_config() -> DocumentClientConfig:
    """Build configuration for Azure Document Intelligence."""
    validate_credentials(
        "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
        "AZURE_DOCUMENT_INTELLIGENCE_KEY",
    )
    return DocumentClientConfig(
        provider="azure_document_intelligence",
        credentials={
            "endpoint": os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"],
            "key": os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"],
        },
        endpoint=os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"],
    )


def build_mindee_config() -> DocumentClientConfig:
    """Build configuration for Mindee Invoice OCR."""
    validate_credentials("MINDEE_API_KEY")
    return DocumentClientConfig(
        provider="mindee",
        credentials={"api_key": os.environ["MINDEE_API_KEY"]},
    )


def build_google_docai_config(project_id: str, processor_id: str, location: str = "us") -> DocumentClientConfig:
    """Build configuration for Google Document AI."""
    validate_credentials("GOOGLE_APPLICATION_CREDENTIALS")
    return DocumentClientConfig(
        provider="google_document_ai",
        credentials={
            "project_id": project_id,
            "processor_id": processor_id,
            "location": location,
        },
    )


def build_aws_textract_config() -> DocumentClientConfig:
    """Build configuration for Amazon Textract."""
    validate_credentials("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY")
    return DocumentClientConfig(
        provider="aws_textract",
        credentials={
            "aws_access_key_id": os.environ["AWS_ACCESS_KEY_ID"],
            "aws_secret_access_key": os.environ["AWS_SECRET_ACCESS_KEY"],
        },
    )


def get_client_for_provider(provider: str) -> DocumentClientConfig:
    """Factory to build client config based on provider name."""
    providers = {
        "azure_document_intelligence": build_azure_di_config,
        "mindee": build_mindee_config,
        "google_document_ai": lambda: build_google_docai_config(
            os.environ.get("GCP_PROJECT_ID", ""),
            os.environ.get("GCP_PROCESSOR_ID", ""),
            os.environ.get("GCP_PROCESSOR_LOCATION", "us"),
        ),
        "aws_textract": build_aws_textract_config,
    }
    if provider not in providers:
        raise ValueError(f"Unsupported provider: {provider}")
    return providers[provider]()


def format_field_value(value: Any, confidence: Optional[float] = None) -> Dict[str, Any]:
    """Format an extracted field with optional confidence score."""
    result = {"value": value}
    if confidence is not None:
        result["confidence"] = round(confidence, 4)
    return result


def normalize_amount(amount_str: Optional[str]) -> Optional[float]:
    """Normalize a currency amount string to float."""
    if not amount_str:
        return None
    cleaned = amount_str.replace("$", "").replace(",", "").replace(" ", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return None


def normalize_date(date_str: Optional[str]) -> Optional[str]:
    """Normalize a date string to ISO format (best-effort)."""
    if not date_str:
        return None
    from datetime import datetime
    formats = [
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%Y/%m/%d",
        "%B %d, %Y",
        "%b %d, %Y",
        "%d %B %Y",
        "%d %b %Y",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return date_str.strip()
