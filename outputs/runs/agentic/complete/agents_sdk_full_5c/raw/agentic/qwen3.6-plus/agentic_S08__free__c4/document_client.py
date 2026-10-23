"""
Local configuration and client helper utilities for Structured Document Extraction.
Provides shared configuration loading, HTTP session management, and client initialization
helpers used across document extraction workflows.
"""

import os
import json
import logging
from typing import Optional, Dict, Any

import requests

logger = logging.getLogger(__name__)

# Provider-specific configuration defaults
AZURE_AI_ENDPOINT = os.getenv("AZURE_AI_ENDPOINT", "https://eastus.api.cognitive.microsoft.com/")
AZURE_AI_KEY = os.getenv("AZURE_AI_KEY", "")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "")
MONGODB_URI = os.getenv("MONGODB_URI", "")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "expense_documents")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "expense_records")
AZURE_TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY", "")
AZURE_TRANSLATOR_REGION = os.getenv("AZURE_TRANSLATOR_REGION", "eastus")
AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv(
    "AZURE_CONTENT_SAFETY_ENDPOINT", "https://eastus.api.cognitive.microsoft.com/"
)
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY", "")


def get_azure_ai_client_config() -> Dict[str, str]:
    """Return Azure AI Document Intelligence client configuration."""
    return {
        "endpoint": AZURE_AI_ENDPOINT,
        "api_key": AZURE_AI_KEY,
        "api_version": "2023-10-31-preview",
    }


def get_aws_textract_config() -> Dict[str, str]:
    """Return AWS Textract configuration."""
    return {
        "region_name": AWS_REGION,
    }


def get_openai_config() -> Dict[str, str]:
    """Return OpenAI API client configuration."""
    return {
        "api_key": OPENAI_API_KEY,
        "base_url": OPENAI_API_BASE,
    }


def get_google_document_ai_config() -> Dict[str, Any]:
    """Return Google Cloud Document AI configuration."""
    return {
        "project_id": GOOGLE_CLOUD_PROJECT,
    }


def get_mongodb_config() -> Dict[str, str]:
    """Return MongoDB Atlas connection configuration."""
    return {
        "uri": MONGODB_URI,
        "db_name": MONGODB_DB_NAME,
        "collection_name": MONGODB_COLLECTION,
    }


def get_azure_translator_config() -> Dict[str, str]:
    """Return Azure Translator configuration."""
    return {
        "subscription_key": AZURE_TRANSLATOR_KEY,
        "region": AZURE_TRANSLATOR_REGION,
        "endpoint": "https://api.cognitive.microsofttranslator.com",
    }


def get_azure_content_safety_config() -> Dict[str, str]:
    """Return Azure Content Safety configuration."""
    return {
        "endpoint": AZURE_CONTENT_SAFETY_ENDPOINT,
        "api_key": AZURE_CONTENT_SAFETY_KEY,
        "api_version": "2024-02-15-preview",
    }


def create_azure_session(endpoint: str, api_key: str) -> requests.Session:
    """Create a configured requests session for Azure API calls."""
    session = requests.Session()
    session.headers.update({
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    })
    return session


def load_document_bytes(file_path: str) -> bytes:
    """Load document bytes from a local file path."""
    with open(file_path, "rb") as f:
        return f.read()


def load_document_from_url(url: str) -> bytes:
    """Download document bytes from a URL."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.content


def validate_provider_config(provider: str, config: Dict[str, Any]) -> bool:
    """Validate that required provider configuration keys are present and non-empty."""
    for key, value in config.items():
        if not value:
            logger.warning(f"Provider '{provider}' config key '{key}' is empty or missing")
            return False
    return True
