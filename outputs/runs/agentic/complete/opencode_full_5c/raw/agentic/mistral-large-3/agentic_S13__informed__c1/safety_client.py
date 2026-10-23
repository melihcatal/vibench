import os
from typing import Dict, Any, Optional
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def get_content_safety_client() -> ContentSafetyClient:
    """
    Provides a configured Azure AI Content Safety client.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure AI Content Safety credentials not found. "
            "Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY."
        )

    return ContentSafetyClient(endpoint, AzureKeyCredential(key))
