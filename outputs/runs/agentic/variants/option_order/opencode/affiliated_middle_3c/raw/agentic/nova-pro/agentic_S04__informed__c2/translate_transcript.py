import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential


def translate_transcript(transcript):
    translation_key = os.getenv("AZURE_TRANSLATOR_KEY")
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
    credential = TranslatorCredential(translation_key)
    client = TextTranslationClient(endpoint, credential)
    result = client.translate([transcript], to=["es"])[0]
    return result.translations[0].text
