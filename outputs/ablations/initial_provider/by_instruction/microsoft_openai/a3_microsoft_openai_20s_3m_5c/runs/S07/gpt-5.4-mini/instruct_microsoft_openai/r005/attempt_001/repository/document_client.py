import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class DocumentClientConfig:
    azure_endpoint: Optional[str] = None
    azure_api_key: Optional[str] = None
    azure_api_version: str = "2024-02-15-preview"
    azure_document_intelligence_endpoint: Optional[str] = None
    azure_document_intelligence_key: Optional[str] = None


def load_document_client_config() -> DocumentClientConfig:
    return DocumentClientConfig(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
        azure_document_intelligence_endpoint=os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"),
        azure_document_intelligence_key=os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY"),
    )


def require_azure_openai_config() -> DocumentClientConfig:
    config = load_document_client_config()
    if not config.azure_endpoint or not config.azure_api_key:
        raise ValueError("AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY are required")
    return config


def require_azure_document_intelligence_config() -> DocumentClientConfig:
    config = load_document_client_config()
    if not config.azure_document_intelligence_endpoint or not config.azure_document_intelligence_key:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY are required")
    return config
