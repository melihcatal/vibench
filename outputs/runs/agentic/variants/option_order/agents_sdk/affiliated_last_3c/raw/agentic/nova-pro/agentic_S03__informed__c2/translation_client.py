import os
from azure.ai.translation.text import TextTranslationClient

def get_translation_client():
    endpoint = os.getenv('AZURE_TRANSLATOR_ENDPOINT')
    key = os.getenv('AZURE_TRANSLATOR_KEY')
    return TextTranslationClient(endpoint=endpoint, credential=key