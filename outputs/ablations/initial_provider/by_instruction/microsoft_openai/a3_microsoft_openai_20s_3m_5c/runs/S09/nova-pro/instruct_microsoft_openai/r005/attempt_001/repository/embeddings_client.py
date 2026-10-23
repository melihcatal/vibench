import os
from openai import AzureOpenAI

def get_client() -> AzureOpenAI:
    return AzureOpenAI(
        api_key=os.getenv('AZURE_OPENAI_API_KEY'),
        api_version='2023-05-15',
        azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
    )