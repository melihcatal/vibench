"""
consent_translate.py - Translate identity-provider consent copy into
multiple languages for international federated login flows.

Provider: DeepL API
SDK: deepl
Auth env vars: DEEPL_AUTH_KEY
"""

import os
from typing import Optional

import deepl


# Common consent text templates for identity providers
DEFAULT_CONSENT_TEMPLATES = {
    "en": {
        "consent_title": "Sign in with {provider}",
        "consent_body": (
            "{app_name} is requesting access to your {provider} account. "
            "You will be able to review the permissions before confirming."
        ),
        "consent_scopes": "Requested permissions:",
        "consent_confirm": "Allow access",
        "consent_deny": "Deny",
        "privacy_notice": (
            "By continuing, you agree to share the requested information "
            "with {app_name} in accordance with their privacy policy."
        ),
    },
}

# Target languages for translation
SUPPORTED_TARGET_LANGUAGES = [
    "de",  # German
    "es",  # Spanish
    "fr",  # French
    "ja",  # Japanese
    "pt",  # Portuguese
    "zh",  # Chinese
    "ko",  # Korean
    "it",  # Italian
    "nl",  # Dutch
    "pl",  # Polish
]


def get_deepl_client() -> deepl.Translator:
    """
    Create a DeepL translator client using the DEEPL_AUTH_KEY
    environment variable.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY", "")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set")
    return deepl.Translator(auth_key)


def translate_consent_text(
    text: str,
    target_language: str,
    source_language: str = "en",
    formality: Optional[str] = None,
) -> str:
    """
    Translate a single consent text string using the DeepL API.

    Args:
        text: The English consent text to translate.
        target_language: Target language code (e.g., 'de', 'es', 'fr').
        source_language: Source language code (default: 'en').
        formality: 'more' for formal, 'less' for informal, or None for default.

    Returns:
        Translated text string.
    """
    translator = get_deepl_client()

    kwargs: dict = {
        "target_lang": target_language.upper(),
        "source_lang": source_language.upper() if source_language != "en" else None,
    }

    if formality:
        kwargs["formality"] = formality

    result = translator.translate_text(text, **kwargs)
    return result.text


def translate_consent_page(
    provider_name: str,
    app_name: str,
    target_language: str,
    templates: Optional[dict] = None,
) -> dict:
    """
    Translate all consent page copy for a federated login flow
    into the target language using DeepL.

    Returns a dict with all translated consent text keys.
    """
    source_templates = templates or DEFAULT_CONSENT_TEMPLATES["en"]

    # Format templates with provider and app names before translation
    formatted_templates = {}
    for key, template in source_templates.items():
        formatted_templates[key] = template.format(
            provider=provider_name,
            app_name=app_name,
        )

    translated = {}
    for key, text in formatted_templates.items():
        translated[key] = translate_consent_text(
            text=text,
            target_language=target_language,
            source_language="en",
        )

    translated["_target_language"] = target_language
    translated["_provider"] = provider_name
    translated["_app_name"] = app_name

    return translated


def translate_consent_all_languages(
    provider_name: str,
    app_name: str,
    target_languages: Optional[list[str]] = None,
) -> dict:
    """
    Translate consent copy into all supported target languages
    using the DeepL Translation API.

    Returns a dict mapping language codes to translated consent pages.
    """
    languages = target_languages or SUPPORTED_TARGET_LANGUAGES
    all_translations = {}

    for lang in languages:
        all_translations[lang] = translate_consent_page(
            provider_name=provider_name,
            app_name=app_name,
            target_language=lang,
        )

    return all_translations


def translate_scopes_description(
    scopes: list[str],
    target_language: str,
    source_language: str = "en",
) -> dict[str, str]:
    """
    Translate a list of OAuth scope descriptions using DeepL.

    Returns a dict mapping original scopes to their translations.
    """
    translated = {}
    for scope in scopes:
        translated[scope] = translate_consent_text(
            text=scope,
            target_language=target_language,
            source_language=source_language,
        )
    return translated
