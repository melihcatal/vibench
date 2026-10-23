import os
from azure.ai.translation.text import TextTranslationClient, TextTranslationInput


def translate_script(script: str, to_language: str) -> str:
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
    client = TextTranslationClient(endpoint=endpoint, credential=key)
    result = client.translate([TextTranslationInput(text=script, to=[to_language])])
    return result[0].translations[0].text
