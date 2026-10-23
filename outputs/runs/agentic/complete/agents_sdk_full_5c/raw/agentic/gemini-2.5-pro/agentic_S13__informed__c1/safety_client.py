import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

def get_azure_safety_client() -> ContentSafetyClient:
    """

    Retrieves Azure credentials from environment variables and
    initializes the ContentSafetyClient.
    """
    try:
        endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
        key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    except KeyError as e:
        raise ValueError(
            f"Missing required environment variable: {e}"
        ) from e

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    return client
