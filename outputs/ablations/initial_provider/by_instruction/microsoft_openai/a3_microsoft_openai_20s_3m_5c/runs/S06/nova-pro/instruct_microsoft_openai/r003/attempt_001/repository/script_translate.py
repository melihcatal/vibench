import os
from azure.cognitiveservices.translation.text import TextTranslationClient, TextTranslationInput

def translate_script(script: str, target_language: str) -> str:
    subscription_key = os.getenv('AZURE_TRANSLATE_KEY')
    endpoint = os.getenv('AZURE_TRANSLATE_ENDPOINT')
    client = TextTranslationClient(endpoint, subscription_key)
    result = client.translate([TextTranslationInput(script, target_language)])
    return result[0].translations[0].text