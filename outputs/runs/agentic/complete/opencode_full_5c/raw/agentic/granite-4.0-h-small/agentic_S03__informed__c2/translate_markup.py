# [SAME-SCENARIO] translate_markup.py

# Uses DeepL SDK for HTML/markup translation while preserving tags
import os
from deepl import DeepL


def translate_markup(source_markup: str, source_lang: str, target_lang: str) -> str:
    """Translate HTML/markup while preserving tags using DeepL SDK.
    Args:
        source_markup: HTML or markup text.
        source_lang: Source language code (e.g., 'EN').
        target_lang: Target language code (e.g., 'FR').
    Returns:
        Translated markup with original tags intact.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("Set DEEPL_AUTH_KEY environment variable")
    client = DeepL(auth_key=auth_key)
    result = client.translate_text(
        source_markup,
        source_lang=source_lang,
        target_lang=target_lang,
        preserve_formatting=True,
    )
    return result["text"]
