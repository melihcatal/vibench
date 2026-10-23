import os
from openai import AzureOpenAI

def get_model_client() -> AzureOpenAI:
    """
    Initializes and returns an Azure OpenAI client using environment variables.
    """
    return AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )