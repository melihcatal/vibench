import os
from openai import AzureOpenAI

def get_azure_openai_client():
    """Initializes and returns an AzureOpenAI client."""
    return AzureOpenAI(
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01"),
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        api_key=os.environ.get("AZURE_OPENAI_API_KEY")
    )
