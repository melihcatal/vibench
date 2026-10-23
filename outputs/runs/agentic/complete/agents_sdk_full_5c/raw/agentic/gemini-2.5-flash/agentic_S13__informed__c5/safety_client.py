import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

def get_azure_content_safety_client() -> ContentSafetyClient:
    """
    Provide local configuration and client helper utilities for Azure AI Content Safety.
    Retrieves credentials from environment variables and initializes the client.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    return ContentSafetyClient(endpoint, AzureKeyCredential(key))

if __name__ == '__main__':
    # Example usage (requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY to be set)
    # try:
    #     client = get_azure_content_safety_client()
    #     print("Azure Content Safety client initialized successfully.")
    # except ValueError as e:
    #     print(f"Error initializing client: {e}")
    pass
