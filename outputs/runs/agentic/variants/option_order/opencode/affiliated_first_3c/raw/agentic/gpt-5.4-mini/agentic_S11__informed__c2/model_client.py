import os
from openai import AzureOpenAI

def get_client():
    return AzureOpenAI(api_key=os.environ['AZURE_OPENAI_API_KEY'], azure_endpoint=os.environ['AZURE_OPENAI_ENDPOINT'], api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2024-06-01'))
