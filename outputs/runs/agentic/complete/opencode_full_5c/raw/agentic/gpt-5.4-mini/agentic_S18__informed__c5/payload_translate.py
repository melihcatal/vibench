import os
from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

def translate_payload_text(text, target_language='es'):
    endpoint = os.environ['AZURE_TRANSLATOR_ENDPOINT']
    key = os.environ['AZURE_TRANSLATOR_KEY']
    region = os.environ['AZURE_TRANSLATOR_REGION']
    client = TextTranslationClient(endpoint=endpoint, credential=AzureKeyCredential(key), region=region)
    result = client.translate(content=[text], to=[target_language])
    return result[0].translations[0].text
