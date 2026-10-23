import os
from openai import AzureOpenAI

def get_client():
    return AzureOpenAI(
        api_key=os.getenv('AZURE_OPENAI_API_KEY'),
        api_version='2023-03-15-preview',
        azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
    )