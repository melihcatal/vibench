import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

# Azure Content Safety specific environment variables
AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

_content_safety_client = None

def get_content_safety_client() -> ContentSafetyClient:
    """
    Provides a singleton instance of the Azure Content Safety client.
    Requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY to be set in environment variables.
    """
    global _content_safety_client
    if _content_safety_client is None:
        if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
            raise ValueError(
                "Azure Content Safety endpoint and key must be set in "
                "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables."
            )
        _content_safety_client = ContentSafetyClient(
            endpoint=AZURE_CONTENT_SAFETY_ENDPOINT,
            credential=AzureKeyCredential(AZURE_CONTENT_SAFETY_KEY)
        )
    return _content_safety_client
