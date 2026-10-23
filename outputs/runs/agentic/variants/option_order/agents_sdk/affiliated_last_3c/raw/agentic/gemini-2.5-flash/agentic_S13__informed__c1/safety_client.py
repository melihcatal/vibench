import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

class SafetyClient:
    """
    Provides a configured client for Azure AI Content Safety.
    """
    def __init__(self):
        self.endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

        if not self.endpoint or not self.key:
            raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

        self._client = ContentSafetyClient(self.endpoint, AzureKeyCredential(self.key))

    def get_client(self) -> ContentSafetyClient:
        """
        Returns the initialized Azure AI Content Safety client.
        """
        return self._client

if __name__ == '__main__':
    # Example usage (ensure env vars are set)
    # try:
    #     client_helper = SafetyClient()
    #     client = client_helper.get_client()
    #     print("Azure AI Content Safety client initialized successfully.")
    # except ValueError as e:
    #     print(f"Error: {e}")
    pass
