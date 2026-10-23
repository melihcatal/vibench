import os
from openai import AzureOpenAI


def get_platform_client() -> AzureOpenAI:
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    if not api_key or not azure_endpoint:
        raise ValueError("AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT must be set")
    return AzureOpenAI(
        api_key=api_key,
        azure_endpoint=azure_endpoint,
        api_version="2024-02-15-preview",
    )
