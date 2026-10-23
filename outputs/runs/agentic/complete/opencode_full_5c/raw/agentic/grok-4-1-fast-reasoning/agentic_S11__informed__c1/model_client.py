import os
from openai import AzureOpenAI


def get_client():
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    if not endpoint or not api_key:
        raise ValueError("AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY are required")
    return AzureOpenAI(
        azure_endpoint=endpoint, api_key=api_key, api_version="2024-02-15-preview"
    )
