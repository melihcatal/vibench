"""
Translate identity-provider consent copy using the DeepL Translation API.
Localizes OAuth consent screen text for federated login across multiple languages.
"""

import os
from typing import Optional, Dict, Any, List

import deepl


DEEPL_API_KEY = os.getenv("DEEPL_API_KEY", "")
DEEPL_API_URL = os.getenv("DEEPL_API_URL", "https://api.deepl.com/v2/translate")


class TranslationError(Exception):
    """Raised when translation fails."""
    pass


def translate_consent_text(
    text: str,
    target_lang: str = "ES",
    source_lang: Optional[str] = None,
    api_key: Optional[str] = None,
    formality: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate a single consent text string using DeepL API.

    Supports formality levels for languages that distinguish formal/informal.
    """
    translator = deepl.Translator(
        api_key or DEEPL_API_KEY,
        server_url=DEEPL_API_URL if "deepl.com" not in DEEPL_API_URL else None,
    )

    try:
        kwargs: Dict[str, Any] = {"target_lang": target_lang}
        if source_lang:
            kwargs["source_lang"] = source_lang
        if formality:
            kwargs["formality"] = formality

        result = translator.translate_text(text, **kwargs)

        return {
            "translated_text": result.text,
            "source_lang": result.detected_source_lang,
            "target_lang": target_lang,
            "formality": formality,
            "provider": "deepl",
            "api_endpoint": DEEPL_API_URL,
        }

    except deepl.DeepLException as exc:
        raise TranslationError(f"DeepL translation failed: {exc}") from exc


def translate_consent_bundle(
    consent_texts: Dict[str, str],
    target_lang: str = "ES",
    source_lang: Optional[str] = None,
    api_key: Optional[str] = None,
    formality: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate multiple consent text fields as a batch using DeepL.

    Typical consent fields include title, description, terms, and action labels.
    """
    translator = deepl.Translator(
        api_key or DEEPL_API_KEY,
        server_url=DEEPL_API_URL if "deepl.com" not in DEEPL_API_URL else None,
    )

    texts = [consent_texts[key] for key in consent_texts if consent_texts[key]]
    keys = [key for key in consent_texts if consent_texts[key]]

    if not texts:
        return {
            "translations": {},
            "target_lang": target_lang,
            "provider": "deepl",
        }

    try:
        kwargs: Dict[str, Any] = {"target_lang": target_lang}
        if source_lang:
            kwargs["source_lang"] = source_lang
        if formality:
            kwargs["formality"] = formality

        results = translator.translate_text(texts, **kwargs)

        translations = {}
        for key, result in zip(keys, results):
            translations[key] = result.text

        return {
            "translations": translations,
            "source_lang": results[0].detected_source_lang if results else None,
            "target_lang": target_lang,
            "formality": formality,
            "provider": "deepl",
            "api_endpoint": DEEPL_API_URL,
            "fields_translated": len(translations),
        }

    except deepl.DeepLException as exc:
        raise TranslationError(f"DeepL batch translation failed: {exc}") from exc


def translate_auth0_consent_screen(
    client_name: str = "My Application",
    scopes: Optional[List[str]] = None,
    target_lang: str = "ES",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate an Auth0-style consent screen to a target language.

    Generates and translates the standard consent copy shown during
    OAuth authorization.
    """
    scope_list = scopes or ["openid", "profile", "email"]
    scope_descriptions = {
        "openid": "Verify your identity",
        "profile": "Access your profile information",
        "email": "Access your email address",
    }

    consent_bundle = {
        "title": f"{client_name} would like to access your account",
        "description": "This application needs the following permissions:",
        "scopes": ", ".join(
            scope_descriptions.get(s, s) for s in scope_list
        ),
        "terms": "By continuing, you agree to our Terms of Service and Privacy Policy.",
        "allow_button": "Allow",
        "deny_button": "Deny",
    }

    return translate_consent_bundle(
        consent_texts=consent_bundle,
        target_lang=target_lang,
        api_key=api_key,
        formality="default",
    )


def get_supported_languages(api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Fetch supported languages from DeepL API.
    """
    translator = deepl.Translator(
        api_key or DEEPL_API_KEY,
        server_url=DEEPL_API_URL if "deepl.com" not in DEEPL_API_URL else None,
    )

    try:
        target_languages = translator.get_target_languages()
        source_languages = translator.get_source_languages()

        return {
            "target_languages": [
                {"code": lang.code, "name": lang.name}
                for lang in target_languages
            ],
            "source_languages": [
                {"code": lang.code, "name": lang.name}
                for lang in source_languages
            ],
            "provider": "deepl",
            "api_endpoint": DEEPL_API_URL,
        }

    except deepl.DeepLException as exc:
        raise TranslationError(f"DeepL language fetch failed: {exc}") from exc


if __name__ == "__main__":
    result = translate_consent_text(
        "This application would like to access your profile and email.",
        target_lang="DE",
    )
    print(f"Translated: {result['translated_text']}")
    print(f"Provider: {result['provider']}")
