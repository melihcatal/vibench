import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def get_content_safety_client() -> ContentSafetyClient:
    """Initialize and return Azure AI Content Safety client."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety endpoint and key must be set.")

    return ContentSafetyClient(endpoint, AzureKeyCredential(key))