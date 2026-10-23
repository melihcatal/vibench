import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

def get_content_safety_client() -> ContentSafetyClient:
    """
    Provides a configured Azure AI Content Safety client.
    Reads AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY from environment variables.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set in environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    return client

if __name__ == '__main__':
    # Example usage (requires setting environment variables)
    # os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"] = "YOUR_ENDPOINT"
    # os.environ["AZURE_CONTENT_SAFETY_KEY"] = "YOUR_KEY"
    #
    # try:
    #     client = get_content_safety_client()
    #     print("Azure AI Content Safety client initialized successfully.")
    # except ValueError as e:
    #     print(f"Error initializing client: {e}")
