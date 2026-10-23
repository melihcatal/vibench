"""
Local configuration and client helper utilities for Text Content Safety.
Provider: Azure AI Content Safety (azure-ai-contentsafety SDK).
"""

import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from typing import Optional


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")


def get_content_safety_client(
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> ContentSafetyClient:
    """Create and return an Azure AI Content Safety client instance."""
    ep = endpoint or AZURE_CONTENT_SAFETY_ENDPOINT
    key = api_key or AZURE_CONTENT_SAFETY_KEY

    if not ep or not key:
        raise ValueError(
            "Azure Content Safety credentials required. "
            "Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY."
        )

    credential = AzureKeyCredential(key)
    client = ContentSafetyClient(endpoint=ep, credential=credential)
    return client


def validate_client(client: ContentSafetyClient) -> bool:
    """Validate that the client can reach the Azure Content Safety service."""
    try:
        from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
        options = AnalyzeTextOptions(
            text="validation test",
            categories=[TextCategory.HATE, TextCategory.SELF_HARM],
        )
        client.analyze_text(options=options)
        return True
    except HttpResponseError:
        return False


def get_provider_name() -> str:
    """Return the provider identifier for this safety integration."""
    return "Azure AI Content Safety"


def get_provider_env_vars() -> dict:
    """Return the environment variables used by this provider."""
    return {
        "AZURE_CONTENT_SAFETY_ENDPOINT": AZURE_CONTENT_SAFETY_ENDPOINT,
        "AZURE_CONTENT_SAFETY_KEY": "***" if AZURE_CONTENT_SAFETY_KEY else "",
    }
