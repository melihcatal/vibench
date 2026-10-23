import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def get_safety_client() -> ContentSafetyClient:
    """
    Initializes and returns a ContentSafetyClient.
    """
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    if not endpoint or not key:
        raise ValueError(
            "Azure Content Safety endpoint and key must be set in environment variables."
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    return client
