import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-05-15',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def translate_text(text, target_language):
    response = client.translations.create(
        model='text-davinci-003',
        source_text=text,
        target_language=target_language
    )
    return response.translated_text.strip()