"""
[LATER-STEP] Translate onboarding copy into the user's locale.

Provider: DeepL API
- SDK: deepl
- Auth: DEEPL_AUTH_KEY
"""

import os
from typing import Dict, List, Optional

import deepl


ONBOARDING_COPY = {
    "welcome_title": "Welcome to our platform!",
    "welcome_body": "We are excited to have you on board. Please complete your profile to get started.",
    "next_steps_title": "Your Next Steps",
    "next_steps_body": "Upload a profile photo, set your preferences, and explore the dashboard.",
}

LOCALE_TO_DEEPL_LANG = {
    "en": "EN",
    "de": "DE",
    "fr": "FR",
    "es": "ES",
    "it": "IT",
    "pt": "PT-BR",
    "ja": "JA",
    "zh": "ZH",
    "nl": "NL",
    "pl": "PL",
    "ru": "RU",
}


def _get_deepl_target_language(locale: str) -> str:
    """Map a user locale to a DeepL target language code."""
    base = locale.split("-")[0].lower()
    return LOCALE_TO_DEEPL_LANG.get(base, base.upper())


def translate_onboarding_copy(
    target_locale: str,
    custom_copy: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    """Translate onboarding strings into the user's locale using DeepL API.

    Uses the DeepL Python SDK (deepl) with free/pro plan API.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY", "").strip()
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required for DeepL API access")

    copy = custom_copy or ONBOARDING_COPY
    target_lang = _get_deepl_target_language(target_locale)

    translator = deepl.Translator(auth_key)
    texts = list(copy.values())

    results = translator.translate_text(
        texts,
        target_lang=target_lang,
        source_lang=None,
    )

    translated = {}
    for key, result in zip(copy.keys(), results):
        translated[key] = result.text

    return translated


def translate_text(text: str, target_locale: str, source_locale: Optional[str] = None) -> str:
    """Translate a single text string using DeepL API."""
    auth_key = os.environ.get("DEEPL_AUTH_KEY", "").strip()
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required for DeepL API access")

    target_lang = _get_deepl_target_language(target_locale)
    source_lang = None
    if source_locale:
        base = source_locale.split("-")[0].upper()
        source_lang = base if base in {"EN", "DE", "FR", "ES", "IT", "PT", "JA", "ZH", "NL", "PL", "RU"} else None

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang, source_lang=source_lang)
    return result.text


if __name__ == "__main__":
    translated = translate_onboarding_copy("de")
    for key, value in translated.items():
        print(f"{key}: {value}")
