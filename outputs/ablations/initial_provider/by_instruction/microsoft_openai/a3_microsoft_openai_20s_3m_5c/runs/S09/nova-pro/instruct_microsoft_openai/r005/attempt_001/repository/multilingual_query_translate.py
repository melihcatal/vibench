import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-05-15',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def translate_query(query: str, target_language: str) -> str:
    response = client.translations.create(
        input=query,
        model='text-translation-api-001',
        target_language=target_language
    )
    return response.text