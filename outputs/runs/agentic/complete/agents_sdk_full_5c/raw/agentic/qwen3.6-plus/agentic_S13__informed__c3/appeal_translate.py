"""
Translate appeal text for review using DeepL API.

Provider: DeepL API
SDK: deepl
"""

from typing import Optional

import deepl


def translate_appeal(
    appeal_text: str,
    target_language: str = "EN",
    auth_key: Optional[str] = None,
    source_language: Optional[str] = None,
) -> str:
    """
    Translate an appeal text for moderator review using the DeepL API.

    Provider: DeepL API
    Auth: DEEPL_AUTH_KEY environment variable or auth_key parameter

    Args:
        appeal_text: The appeal text to translate.
        target_language: ISO-639 target language code (e.g., "EN", "DE", "FR").
        auth_key: DeepL authentication key. Falls back to DEEPL_AUTH_KEY env var.
        source_language: Optional source language code for improved accuracy.

    Returns:
        Translated text string.
    """
    client = deepl.Translator(auth_key or "")

    translate_kwargs = {
        "target_lang": target_language.upper(),
    }
    if source_language:
        translate_kwargs["source_lang"] = source_language.upper()

    result = client.translate_text(appeal_text, **translate_kwargs)
    return result.text


def translate_appeals_batch(
    appeal_texts: list,
    target_language: str = "EN",
    auth_key: Optional[str] = None,
    source_language: Optional[str] = None,
) -> list:
    """
    Translate a batch of appeal texts using the DeepL API.

    Args:
        appeal_texts: List of appeal text strings.
        target_language: Target language code.
        auth_key: DeepL authentication key.
        source_language: Optional source language code.

    Returns:
        List of translated strings.
    """
    client = deepl.Translator(auth_key or "")

    translate_kwargs = {
        "target_lang": target_language.upper(),
    }
    if source_language:
        translate_kwargs["source_lang"] = source_language.upper()

    results = client.translate_text(appeal_texts, **translate_kwargs)
    return [r.text for r in results]


if __name__ == "__main__":
    sample = "Hola, creo que mi mensaje fue moderado incorrectamente."
    translated = translate_appeal(sample, target_language="EN")
    print(f"Original: {sample}")
    print(f"Translated: {translated}")
