import os

from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-07-01-preview',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def embed_output(output):
    # Placeholder for embedding logic
    return output