"""
Local configuration and client helper utilities for Text Content Safety.
Provider: Azure AI Content Safety
"""

import os
from typing import Optional

from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def get_content_safety_endpoint() -> str:
    """Retrieve the Azure AI Content Safety endpoint from environment."""
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    if not endpoint:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT environment variable is required")
    return endpoint


def get_content_safety_key() -> str:
    """Retrieve the Azure AI Content Safety API key from environment."""
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not key:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is required")
    return key


def create_content_safety_client(
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> ContentSafetyClient:
    """
    Create and return an authenticated Azure AI Content Safety client.

    Args:
        endpoint: Azure Content Safety endpoint URL. Falls back to env var.
        key: Azure Content Safety API key. Falls back to env var.

    Returns:
        Configured ContentSafetyClient instance.
    """
    endpoint = endpoint or get_content_safety_endpoint()
    key = key or get_content_safety_key()
    credential = AzureKeyCredential(key)
    return ContentSafetyClient(endpoint=endpoint, credential=credential)
