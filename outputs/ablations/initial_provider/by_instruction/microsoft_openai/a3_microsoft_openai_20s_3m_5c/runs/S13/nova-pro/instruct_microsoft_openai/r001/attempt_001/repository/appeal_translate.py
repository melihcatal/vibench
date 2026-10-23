import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-05-15',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def translate_appeal(text, target_language='es'):
    response = client.translations.create(
        input=text,
        target_language=target_language,
        model='text-translation-001'
    )
    return response.text