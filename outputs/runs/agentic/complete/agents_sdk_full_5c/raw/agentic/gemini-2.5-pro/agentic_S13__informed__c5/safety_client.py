import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

_client = None

def get_safety_client() -> ContentSafetyClient:
    """
    Initializes and returns a singleton ContentSafetyClient.
    """
    global _client
    if _client is None:
        try:
            endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
            key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
            _client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
        except KeyError:
            raise Exception("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")
    return _client
