import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient

class SafetyClient:
    def __init__(self):
        self.endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
        if not self.endpoint or not self.key:
            raise ValueError("Azure Content Safety endpoint and key must be set in environment variables.")
        self.client = ContentSafetyClient(self.endpoint, AzureKeyCredential(self.key))

    def get_client(self) -> ContentSafetyClient:
        return self.client
