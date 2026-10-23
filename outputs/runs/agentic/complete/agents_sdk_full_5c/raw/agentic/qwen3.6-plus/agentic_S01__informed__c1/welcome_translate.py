"""
Translate onboarding copy into the user's locale.

Provider: DeepL API
Provider-identifying signals:
  - deepl SDK import
  - DEEPL_AUTH_KEY environment variable
  - DeepL-specific language codes and formality settings
  - api.deepl.com / v2 translate endpoint
"""

import logging
import os
from typing import Any, Dict, List, Optional

import deepl

from identity_models import serialize_response

logger = logging.getLogger(__name__)

DEEPL_AUTH_KEY_ENV = "DEEPL_AUTH_KEY"

ONBOARDING_COPY_TEMPLATES = {
    "welcome": "Welcome to our platform! We're excited to have you on board.",
    "profile_setup": "Let's set up your profile so other users can get to know you.",
    "email_verification": "Please verify your email address to unlock all features.",
    "first_steps": "Here are a few things you can do to get started:",
    "complete": "You're all set! Start exploring and connecting with others.",
}

DEEPL_LANGUAGE_MAP = {
    "en": "EN-US",
    "en-gb": "EN-GB",
    "en-us": "EN-US",
    "de": "DE",
    "fr": "FR",
    "es": "ES",
    "it": "IT",
    "pt": "PT-PT",
    "pt-br": "PT-BR",
    "ja": "JA",
    "zh": "ZH",
    "ru": "RU",
    "ko": "KO",
    "nl": "NL",
    "pl": "PL",
    "sv": "SV",
    "da": "DA",
    "fi": "FI",
    "hu": "HU",
    "ro": "RO",
    "bg": "BG",
    "cs": "CS",
    "el": "EL",
    "sk": "SK",
    "lt": "LT",
    "lv": "LV",
    "et": "ET",
    "sl": "SL",
    "id": "ID",
    "tr": "TR",
    "uk": "UK",
    "nb": "NB",
}


def _get_deepl_client() -> deepl.Translator:
    """Create a DeepL Translator client using the auth key from environment."""
    auth_key = os.environ.get(DEEPL_AUTH_KEY_ENV)
    if not auth_key:
        raise ValueError(
            f"Missing {DEEPL_AUTH_KEY_ENV}. Set your DeepL API key to use "
            "api.deepl.com translation services."
        )
    return deepl.Translator(auth_key)


def _map_language_code(locale: str) -> str:
    """Map a locale string to a DeepL-supported target language code."""
    code = locale.lower().split("-")[0] if "-" in locale else locale.lower()
    return DEEPL_LANGUAGE_MAP.get(locale.lower(), DEEPL_LANGUAGE_MAP.get(code, "EN-US"))


def translate_onboarding_copy(
    user_locale: str,
    custom_templates: Optional[Dict[str, str]] = None,
    formality: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate onboarding welcome copy into the user's locale using DeepL API.

    Args:
        user_locale: BCP-47 locale code (e.g., 'de', 'fr-FR', 'ja').
        custom_templates: Optional dict of custom text keys and values to
            translate in addition to or instead of the defaults.
        formality: DeepL formality setting ('more', 'less', or 'default').

    Returns:
        Dict with translated onboarding copy keyed by template name.
    """
    client = _get_deepl_client()
    target_lang = _map_language_code(user_locale)

    templates = custom_templates or ONBOARDING_COPY_TEMPLATES

    translate_kwargs: Dict[str, Any] = {
        "target_lang": target_lang,
    }
    if formality:
        translate_kwargs["formality"] = formality

    translated: Dict[str, Any] = {}

    for key, text in templates.items():
        try:
            result = client.translate_text(text, **translate_kwargs)
            translated[key] = result.text
            logger.info(
                "DeepL: Translated '%s' to %s",
                key,
                target_lang,
            )
        except deepl.DeepLException as e:
            logger.error(
                "DeepL API error translating '%s' to %s: %s",
                key,
                target_lang,
                str(e),
            )
            translated[key] = text

    return {
        "locale": user_locale,
        "target_language": target_lang,
        "provider": "deepl",
        "translations": translated,
    }


def translate_onboarding_from_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience wrapper accepting a dict and returning a dict."""
    return translate_onboarding_copy(
        user_locale=data["user_locale"],
        custom_templates=data.get("custom_templates"),
        formality=data.get("formality"),
    )
