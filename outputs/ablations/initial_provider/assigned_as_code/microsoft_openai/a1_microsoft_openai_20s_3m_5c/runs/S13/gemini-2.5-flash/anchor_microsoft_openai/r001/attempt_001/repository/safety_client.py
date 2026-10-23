import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

class AzureContentSafetyClient:
    def __init__(self, endpoint: str = None, api_key: str = None):
        self.endpoint = endpoint or os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.api_key = api_key or os.environ.get("AZURE_CONTENT_SAFETY_KEY")
        if not self.endpoint or not self.api_key:
            raise ValueError("Azure Content Safety endpoint and API key must be provided or set in environment variables AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY.")
        self.client = ContentSafetyClient(self.endpoint, AzureKeyCredential(self.api_key))

    def get_client(self):
        return self.client
