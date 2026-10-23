"""
Translate extracted OCR text using the DeepL API.

Uses the deepl SDK to translate text content previously extracted from
documents via OCR into a target language.
"""

import os
from typing import List, Optional

import deepl


DEEPL_AUTH_KEY_ENV = "DEEPL_AUTH_KEY"


def get_deepl_auth_key() -> str:
    key = os.environ.get(DEEPL_AUTH_KEY_ENV)
    if not key:
        raise ValueError(f"Missing required environment variable: {DEEPL_AUTH_KEY_ENV}")
    return key


def translate_ocr_text(
    text: str,
    target_lang: str = "EN",
    source_lang: Optional[str] = None,
    *,
    auth_key: Optional[str] = None,
) -> str:
    """
    Translate extracted OCR text using the DeepL translation API.

    Args:
        text: The OCR-extracted text to translate.
        target_lang: Target language code (e.g., "EN", "DE", "FR", "JA").
        source_lang: Source language code (optional; DeepL auto-detects if None).
        auth_key: DeepL API key. Falls back to DEEPL_AUTH_KEY.

    Returns:
        The translated text string.
    """
    ak = auth_key or get_deepl_auth_key()
    translator = deepl.Translator(ak)

    translate_kwargs: dict = {"target_lang": target_lang}
    if source_lang:
        translate_kwargs["source_lang"] = source_lang

    result = translator.translate_text(text, **translate_kwargs)
    return result.text


def translate_ocr_texts(
    texts: List[str],
    target_lang: str = "EN",
    *,
    auth_key: Optional[str] = None,
) -> List[str]:
    """
    Translate a list of OCR-extracted text segments using the DeepL API.

    Args:
        texts: List of text strings to translate.
        target_lang: Target language code.
        auth_key: DeepL API key. Falls back to DEEPL_AUTH_KEY.

    Returns:
        List of translated text strings.
    """
    ak = auth_key or get_deepl_auth_key()
    translator = deepl.Translator(ak)

    deepl_texts = [deepl.Text(t) for t in texts]
    results = translator.translate_text(deepl_texts, target_lang=target_lang)
    return [r.text for r in results]


if __name__ == "__main__":
    sample = "Bonjour le monde, ceci est un test de traduction."
    translated = translate_ocr_text(sample, target_lang="EN")
    print(f"Original: {sample}")
    print(f"Translated: {translated}")
