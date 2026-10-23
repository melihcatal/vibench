import os
from translation_client import (
    TranslationClient,
)  # placeholder client for concrete provider


def translate_query(query: str, target_lang: str = "en") -> str:
    """Translate a user query into the target language using a translation provider.

    Default target language is English. Uses Google Cloud Translation as the concrete provider.
    """
    client = TranslationClient()
    client.set_provider("google-cloud-translate")
    translated = client.translate(text=query, target_language=target_lang)
    return translated
