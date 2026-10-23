import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-03-15-preview',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def translate_dashboard_note(note, target_locale):
    response = client.metrics.translate(note=note, target_locale=target_locale)
    return response.translation