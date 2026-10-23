"""Translate onboarding copy into the user's locale using DeepL API.

Uses the DeepL translation SDK to translate onboarding welcome text and UI copy
into the user's detected or selected locale during the account activation flow.
"""

import os
import deepl
from typing import Optional, List


def get_deepl_client() -> deepl.Translator:
    """Create a DeepL Translator client using the DEEPL_AUTH_KEY environment variable.

    Returns:
        deepl.Translator instance configured for the DeepL API.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise EnvironmentError(
            "DEEPL_AUTH_KEY environment variable is required for DeepL translation"
        )
    return deepl.Translator(auth_key)


def translate_onboarding_copy(
    source_text: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
) -> str:
    """Translate onboarding welcome copy into the user's locale via DeepL.

    Args:
        source_text: The onboarding text in the source language.
        target_lang: Target language code (e.g., 'ES', 'JA', 'DE', 'FR').
        source_lang: Optional source language code (e.g., 'EN'). DeepL can
            auto-detect if omitted.
        formality: Optional formality level ('more' or 'less') for languages
            that support it (e.g., German).

    Returns:
        Translated text string.
    """
    client = get_deepl_client()

    translate_kwargs = {
        "target_lang": target_lang.upper(),
    }

    if source_lang:
        translate_kwargs["source_lang"] = source_lang.upper()

    if formality:
        translate_kwargs["formality"] = formality

    result = client.translate_text(source_text, **translate_kwargs)
    return result.text


def translate_onboarding_bundle(
    bundle: dict,
    target_lang: str,
    source_lang: Optional[str] = "EN",
) -> dict:
    """Translate a dictionary of onboarding key-value pairs into the target locale.

    Args:
        bundle: Dictionary mapping copy keys to English source text.
        target_lang: Target language code for DeepL.
        source_lang: Source language code (default 'EN').

    Returns:
        Dictionary with the same keys and translated values.
    """
    translated = {}
    for key, text in bundle.items():
        if text and isinstance(text, str):
            translated[key] = translate_onboarding_copy(
                text, target_lang=target_lang, source_lang=source_lang
            )
        else:
            translated[key] = text
    return translated


def get_supported_target_languages() -> List[str]:
    """Return the list of supported target language codes from DeepL.

    Returns:
        List of uppercase language codes (e.g., ['DE', 'EN', 'ES', 'FR', ...]).
    """
    client = get_deepl_client()
    languages = client.get_target_languages()
    return [lang.code.upper() for lang in languages]
