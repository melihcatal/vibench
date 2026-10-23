import os

from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-07-01-preview',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def collect_metadata(response):
    metadata = {
        'usage': response.usage,
        'model': response.model,
        'id': response.id
    }
    return metadata