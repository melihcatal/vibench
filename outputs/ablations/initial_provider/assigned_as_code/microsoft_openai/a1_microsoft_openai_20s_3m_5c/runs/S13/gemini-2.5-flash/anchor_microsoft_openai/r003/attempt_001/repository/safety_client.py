from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

def get_content_safety_client(endpoint: str, api_key: str) -> ContentSafetyClient:
    """Initializes and returns an Azure Content Safety client."""
    return ContentSafetyClient(endpoint, AzureKeyCredential(api_key))
