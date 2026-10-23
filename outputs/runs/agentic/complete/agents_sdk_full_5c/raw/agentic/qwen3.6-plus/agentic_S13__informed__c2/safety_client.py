"""
safety_client.py - Local configuration and client helper utilities for Text Content Safety.

Uses Azure AI Content Safety as the provider backend.
Provider signals:
  - SDK: azure-ai-contentsafety
  - Env: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
  - Endpoint hostname pattern: .cognitiveservices.azure.com
"""

import os
from typing import Optional

from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def get_content_safety_endpoint() -> str:
    """Return the Azure Content Safety endpoint from environment."""
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    if not endpoint:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT environment variable is required. "
            "Example: https://<resource>.cognitiveservices.azure.com/"
        )
    return endpoint.rstrip("/")


def get_content_safety_key() -> str:
    """Return the Azure Content Safety API key from environment."""
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not key:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is required.")
    return key


def create_content_safety_client() -> ContentSafetyClient:
    """Create and return an authenticated Azure AI Content Safety client."""
    endpoint = get_content_safety_endpoint()
    credential = AzureKeyCredential(get_content_safety_key())
    client = ContentSafetyClient(endpoint=endpoint, credential=credential)
    return client


def get_api_version() -> str:
    """Return the API version used for Azure AI Content Safety calls."""
    return os.environ.get("CONTENT_SAFETY_API_VERSION", "2024-09-01")


def validate_connection(client: Optional[ContentSafetyClient] = None) -> bool:
    """Validate that the Azure Content Safety client can be instantiated."""
    try:
        if client is None:
            client = create_content_safety_client()
        return client is not None
    except Exception:
        return False
