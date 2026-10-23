import os
from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

def translate_text(text, to_language='es'):
    endpoint = os.getenv('TRANSLATION_ENDPOINT')
    key = os.getenv('TRANSLATION_KEY')
    client = TextTranslationClient(endpoint, AzureKeyCredential(key))
    result = client.translate([text], to_language)
    return result[0].translations[0].text