import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

def get_safety_client() -> ContentSafetyClient:
    """
    Creates and returns an Azure AI Content Safety client.

    Reads configuration from environment variables:
    - AZURE_CONTENT_SAFETY_ENDPOINT: The endpoint for the Content Safety resource.
    - AZURE_CONTENT_SAFETY_KEY: The API key for the Content Safety resource.
    """
    try:
        endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
        key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    except KeyError as e:
        raise ConnectionError(f"Missing environment variable: {e}") from e

    if not endpoint or not key:
        raise ConnectionError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")

    # Create a Content Safety client
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    return client
