import os
from azure.ai.translation.text import TextTranslationClient, TextTranslationInput
from azure.core.credentials import AzureKeyCredential

def translate_platform_output(text, to_language='es'):
    endpoint = os.getenv('TRANSLATOR_ENDPOINT')
    key = os.getenv('TRANSLATOR_KEY')
    client = TextTranslationClient(endpoint, AzureKeyCredential(key))
    result = client.translate([TextTranslationInput(text=text, to=to_language)])
    return result[0].translations[0].text