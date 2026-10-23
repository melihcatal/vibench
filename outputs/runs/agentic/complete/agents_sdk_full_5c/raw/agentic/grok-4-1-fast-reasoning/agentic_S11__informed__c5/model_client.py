import os
from openai import AzureOpenAI

def get_client(api_version: str = '2024-08-01-preview') -> AzureOpenAI:
    return AzureOpenAI(
        azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
        api_key=os.getenv('AZURE_OPENAI_API_KEY'),
        api_version=api_version,
    )
