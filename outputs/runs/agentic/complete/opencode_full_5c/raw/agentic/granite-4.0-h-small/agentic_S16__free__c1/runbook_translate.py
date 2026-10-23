# [LATER-STEP] runbook_translate.py
# Translate secret-rotation runbook notes from English to other languages using Azure Translator

import os
from azure.ai.translation import TranslationClient

TRANSLATOR_ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
client = TranslationClient(endpoint=TRANSLATOR_ENDPOINT, credential=TRANSLATOR_KEY)


def translate_runbook(note: str, target_lang: str = "es") -> str:
    """Translate a secret-rotation runbook note.

    Args:
        note: Original runbook note in English.
        target_lang: Destination language code (e.g., 'es' for Spanish).

    Returns:
        Translated note.
    """
    response = client.translate_text(
        text=note, target_language=target_lang, source_language="en"
    )
    return response[0].translations[0].text
