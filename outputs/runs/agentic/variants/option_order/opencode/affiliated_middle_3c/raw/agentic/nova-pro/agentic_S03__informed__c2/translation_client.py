import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential


def get_translation_client():
    credential = TranslatorCredential(os.getenv("AZURE_TRANSLATOR_KEY"))
    client = TextTranslationClient(credential, os.getenv("AZURE_TRANSLATOR_REGION"))
    return client
