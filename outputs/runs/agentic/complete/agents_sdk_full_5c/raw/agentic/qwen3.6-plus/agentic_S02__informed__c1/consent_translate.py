"""
[LATER-STEP] Translate identity-provider consent copy using DeepL API.

Uses the DeepL Translation API (sdk=deepl) to translate OAuth/OIDC consent
screens, privacy notices, and terms of service copy between supported languages.

Required env vars: DEEPL_AUTH_KEY
"""

import logging
from typing import Any, Dict, List, Optional

import deepl

logger = logging.getLogger(__name__)

# Supported language codes for consent copy translation
SUPPORTED_LANGUAGES = [
    "EN", "DE", "FR", "ES", "IT", "NL", "PL", "PT", "RU", "JA", "ZH", "KO", "BG", "CS", "DA",
    "EL", "ET", "FI", "HU", "LV", "LT", "RO", "SK", "SL", "SV", "UK",
]


def translate_text(
    text: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
    formality: Optional[str] = None,
) -> str:
    """
    Translate text using the DeepL Translation API.

    DeepL API endpoint:
        POST https://api.deepl.com/v2/translate

    Required env var: DEEPL_AUTH_KEY
    """
    if not text or not text.strip():
        return text

    target_lang_upper = target_lang.upper()
    if target_lang_upper not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported target language: {target_lang}. Supported: {SUPPORTED_LANGUAGES}")

    translator = deepl.Translator(auth_key)

    translate_options = {}
    if source_lang:
        translate_options["source_lang"] = source_lang.upper()
    if formality:
        translate_options["formality"] = formality

    result = translator.translate_text(text, target_lang=target_lang_upper, **translate_options)

    logger.info(
        "Translated %d characters from DeepL: %s -> %s (detected: %s)",
        len(text),
        source_lang or "auto",
        target_lang_upper,
        result.detected_source_lang,
    )

    return result.text


def translate_consent_copy(
    consent_text: str,
    target_languages: List[str],
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
    formality: Optional[str] = None,
) -> Dict[str, str]:
    """
    Translate consent screen copy into multiple target languages.
    """
    translations: Dict[str, str] = {}

    for lang in target_languages:
        try:
            translated = translate_text(
                consent_text,
                target_lang=lang,
                source_lang=source_lang,
                auth_key=auth_key,
                formality=formality,
            )
            translations[lang.upper()] = translated
        except deepl.DeepLException as exc:
            logger.error("DeepL translation failed for %s: %s", lang, exc)
            translations[lang.upper()] = f"[Translation failed: {exc}]"

    return translations


def translate_idp_consent_bundle(
    provider: str,
    consent_bundle: Dict[str, str],
    target_languages: List[str],
    auth_key: Optional[str] = None,
) -> Dict[str, Dict[str, str]]:
    """
    Translate a full consent copy bundle for an identity provider.

    consent_bundle keys might include:
        - 'title': consent screen title
        - 'description': consent description
        - 'scope_descriptions': scope-specific descriptions
        - 'privacy_notice': privacy policy excerpt
        - 'terms': terms of service excerpt
        - 'confirm_button': button text
        - 'cancel_button': cancel button text
    """
    result: Dict[str, Dict[str, str]] = {}

    for target_lang in target_languages:
        lang_translations: Dict[str, str] = {}
        for key, text in consent_bundle.items():
            try:
                translated = translate_text(text, target_lang=target_lang, auth_key=auth_key)
                lang_translations[key] = translated
            except deepl.DeepLException as exc:
                logger.error("DeepL translation failed for key=%s, lang=%s: %s", key, target_lang, exc)
                lang_translations[key] = text  # fallback to original

        result[target_lang.upper()] = lang_translations

    return result


def get_supported_languages(auth_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get list of supported languages from DeepL API.
    """
    translator = deepl.Translator(auth_key)
    source_languages = translator.get_source_languages()
    target_languages = translator.get_target_languages()

    return {
        "source_languages": [{"code": lang.code, "name": lang.name} for lang in source_languages],
        "target_languages": [{"code": lang.code, "name": lang.name} for lang in target_languages],
        "provider": "deepl",
    }
