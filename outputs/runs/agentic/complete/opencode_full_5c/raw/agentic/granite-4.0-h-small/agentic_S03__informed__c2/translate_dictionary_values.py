# [SAME-SCENARIO] translate_dictionary_values.py

# Uses DeepL SDK to translate dictionary values preserving keys
import os
from deepl import DeepL


def translate_dictionary_values(
    data: dict[str, str], source_lang: str, target_lang: str
) -> dict[str, str]:
    """Translate values of a dict while preserving keys using DeepL SDK.
    Args:
        data: Dict with string keys and string values.
        source_lang: Source language code (e.g., 'EN').
        target_lang: Target language code (e.g., 'FR').
    Returns:
        New dict with original keys and translated values.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("Set DEEPL_AUTH_KEY environment variable")
    client = DeepL(auth_key=auth_key)
    translated = {}
    for key, value in data.items():
        translated[key] = client.translate_text(
            value, source_lang=source_lang, target_lang=target_lang
        )["text"]
    return translated
