import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential


def translate_text(text, from_language, to_language):
    credential = TranslatorCredential(os.getenv("AZURE_TRANSLATOR_KEY"))
    client = TextTranslationClient(credential, os.getenv("AZURE_TRANSLATOR_REGION"))
    result = client.translate([text], from_language, to_language)
    return result[0].translations[0].text
