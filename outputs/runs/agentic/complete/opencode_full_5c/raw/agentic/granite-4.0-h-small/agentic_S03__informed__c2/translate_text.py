# [SAME-SCENARIO] translate_text.py

# Uses DeepL SDK for general text translation
import os
from deepl import DeepL


def translate_text(source_text: str, source_lang: str, target_lang: str) -> str:
    """Translate a single text string using DeepL SDK.
    Args:
        source_text: The text to translate.
        source_lang: Source language code (e.g., 'EN').
        target_lang: Target language code (e.g., 'FR').
    Returns:
        Translated text.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("Set DEEPL_AUTH_KEY environment variable")
    client = DeepL(auth_key=auth_key)
    result = client.translate_text(
        source_text, source_lang=source_lang, target_lang=target_lang
    )
    return result["text"]
