import os
from openai import AzureOpenAI


def get_platform_client() -> AzureOpenAI:
    """
    Local helper to create Azure OpenAI project-scoped client.
    """
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    if not endpoint:
        raise ValueError("AZURE_OPENAI_ENDPOINT environment variable is required")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    if not api_key:
        raise ValueError("AZURE_OPENAI_API_KEY environment variable is required")
    return AzureOpenAI(
        azure_endpoint=endpoint, api_key=api_key, api_version="2024-02-01"
    )
