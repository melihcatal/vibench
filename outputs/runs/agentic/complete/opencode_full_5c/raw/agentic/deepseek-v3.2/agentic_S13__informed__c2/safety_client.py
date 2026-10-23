import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def get_content_safety_client() -> ContentSafetyClient:
    """Provide local configuration and client helper utilities for Text Content Safety."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure Content Safety credentials not found. "
            "Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables."
        )

    credential = AzureKeyCredential(key)
    client = ContentSafetyClient(endpoint=endpoint, credential=credential)

    return client


def validate_content_safety_config() -> bool:
    """Validate that Azure Content Safety configuration is available."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    return bool(endpoint and key)
