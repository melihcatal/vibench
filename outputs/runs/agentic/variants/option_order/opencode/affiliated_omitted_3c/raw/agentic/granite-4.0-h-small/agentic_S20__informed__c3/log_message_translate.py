import os
from typing import List
from observability_models import TranslatePayload
from observability_client import get_translation_client


def translate_messages(messages: List[str], target_locale: str) -> List[str]:
    """Translate a list of log messages to the specified locale using DeepL API.

    The concrete provider used is DeepL (deepl Python SDK).
    """
    client = get_translation_client()
    # DeepL SDK expects a single text at a time; batch via loop
    translated = []
    for msg in messages:
        resp = client.translate_text(text=msg, target_lang=target_locale)
        translated.append(resp.translated_text)
    return translated


# Helper to create the DeepL client – uses DEEPL_AUTH_KEY
def get_translation_client():
    import deepl

    auth_key = os.getenv("DEEPL_AUTH_KEY")
    return deepl.Auth(auth_key).client()
