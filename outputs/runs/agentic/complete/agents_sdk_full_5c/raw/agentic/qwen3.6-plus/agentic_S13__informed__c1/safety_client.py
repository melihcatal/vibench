"""
Local helper: Provide local configuration and client helper utilities
for Text Content Safety using Azure AI Content Safety.
"""

import os
from typing import Optional

from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://<your-resource-name>.cognitiveservices.azure.com/",
)
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")

DEFAULT_CATEGORIES = ["Hate", "SelfHarm", "Sexual", "Violence"]
DEFAULT_OUTPUT_TYPE = "EightSeverityLevels"


def get_safety_client(
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> ContentSafetyClient:
    """Create and return an Azure AI Content Safety client."""
    ep = endpoint or AZURE_CONTENT_SAFETY_ENDPOINT
    key = api_key or AZURE_CONTENT_SAFETY_KEY
    credential = AzureKeyCredential(key)
    return ContentSafetyClient(endpoint=ep, credential=credential)


def get_analysis_categories(category_names: Optional[list[str]] = None) -> list[str]:
    """Return the list of analysis category identifiers."""
    return category_names or DEFAULT_CATEGORIES


def build_client_config() -> dict:
    """Return a dictionary of client configuration values."""
    return {
        "endpoint": AZURE_CONTENT_SAFETY_ENDPOINT,
        "output_type": DEFAULT_OUTPUT_TYPE,
        "categories": DEFAULT_CATEGORIES,
    }
