import os
from typing import Optional
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

_safety_client = None


def get_safety_client() -> ContentSafetyClient:
    """
    Provide local configuration and client helper utilities for Text Content Safety.
    Returns an Azure AI Content Safety client.
    """
    global _safety_client

    if _safety_client is None:
        endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

        if not endpoint or not key:
            raise ValueError(
                "Azure Content Safety credentials not found. "
                "Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables."
            )

        credential = AzureKeyCredential(key)
        _safety_client = ContentSafetyClient(endpoint=endpoint, credential=credential)

    return _safety_client


def configure_client(endpoint: Optional[str] = None, key: Optional[str] = None):
    """
    Configure the safety client with custom credentials.
    """
    global _safety_client

    if endpoint is None:
        endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    if key is None:
        key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Both endpoint and key are required")

    credential = AzureKeyCredential(key)
    _safety_client = ContentSafetyClient(endpoint=endpoint, credential=credential)

    return _safety_client
