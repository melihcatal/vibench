import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential


def batch_translate(texts, from_language, to_language):
    credential = TranslatorCredential(os.getenv("AZURE_TRANSLATOR_KEY"))
    client = TextTranslationClient(credential, os.getenv("AZURE_TRANSLATOR_REGION"))
    result = client.translate(texts, from_language, to_language)
    return [translation.translations[0].text for translation in result]
