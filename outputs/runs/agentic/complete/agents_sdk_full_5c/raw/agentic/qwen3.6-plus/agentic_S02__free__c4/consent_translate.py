"""
Translate identity-provider consent copy using DeepL API.

Provider: DeepL Translation API (https://www.deepl.com/docs-api/translating-text/)
"""

import os
import time
from typing import List, Optional, Dict

import deepl
from deepl import Translator


DEEPL_API_KEY = os.getenv("DEEPL_API_KEY", "")
DEEPL_API_URL = os.getenv("DEEPL_API_URL", "https://api.deepl.com")

# DeepL supports these target languages for consent copy
SUPPORTED_TARGET_LANGUAGES = [
    "EN", "DE", "FR", "ES", "IT", "NL", "PL", "PT", "RU", "JA", "ZH", "BG", "CS", "DA", "EL",
    "ET", "FI", "HU", "ID", "KO", "LT", "LV", "NB", "RO", "SK", "SL", "SV", "TR", "UK",
]


class TranslationError(Exception):
    """Raised when DeepL translation fails."""
    pass


def init_deepl_translator() -> Translator:
    """Initialize DeepL translator client."""
    return Translator(DEEPL_API_KEY, server_url=DEEPL_API_URL)


def translate_consent_text(
    source_text: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
) -> str:
    """
    Translate consent copy using DeepL API.

    Uses DeepL's neural machine translation for high-quality legal/consent text.
    Target language codes: EN, DE, FR, ES, IT, etc. (ISO 639-1 uppercase).
    """
    if not source_text or not source_text.strip():
        return ""

    if target_lang not in SUPPORTED_TARGET_LANGUAGES:
        raise TranslationError(f"Unsupported target language: {target_lang}")

    try:
        translator = init_deepl_translator()

        kwargs = {
            "target_lang": target_lang,
        }

        if source_lang:
            kwargs["source_lang"] = source_lang
        if formality:
            kwargs["formality"] = formality

        result = translator.translate_text(source_text, **kwargs)
        return result.text

    except deepl.exceptions.AuthorizationException as e:
        raise TranslationError(f"DeepL authorization failed: {str(e)}")
    except deepl.exceptions.QuotaExceededException as e:
        raise TranslationError(f"DeepL quota exceeded: {str(e)}")
    except deepl.exceptions.TooManyRequestsException as e:
        raise TranslationError(f"DeepL rate limit exceeded: {str(e)}")
    except Exception as e:
        raise TranslationError(f"DeepL translation failed: {str(e)}")


def translate_consent_for_locales(
    source_text: str,
    target_locales: List[str],
    source_lang: Optional[str] = None,
) -> Dict[str, str]:
    """
    Translate consent copy into multiple locales using DeepL API.

    Returns dict mapping locale codes to translated text.
    """
    translations = {}

    for locale in target_locales:
        # Extract language code from locale (e.g., "de-DE" -> "DE")
        lang_code = locale.split("-")[0].upper()

        if lang_code not in SUPPORTED_TARGET_LANGUAGES:
            translations[locale] = source_text  # Fallback to original
            continue

        try:
            translated = translate_consent_text(
                source_text=source_text,
                target_lang=lang_code,
                source_lang=source_lang,
                formality="more",  # Formal tone for legal consent text
            )
            translations[locale] = translated
        except TranslationError as e:
            translations[locale] = f"[Translation error: {str(e)}]"

    return translations


def prepare_consent_package(
    consent_id: str,
    source_text: str,
    provider: str,
    target_locales: List[str],
    source_lang: Optional[str] = None,
) -> Dict:
    """
    Prepare a complete consent package with translations for all target locales.

    Uses DeepL to translate identity-provider consent copy.
    """
    translations = translate_consent_for_locales(
        source_text=source_text,
        target_locales=target_locales,
        source_lang=source_lang,
    )

    return {
        "consent_id": consent_id,
        "provider": provider,
        "source_text": source_text,
        "source_lang": source_lang or "auto",
        "translations": translations,
        "created_at": int(time.time()),
        "translation_service": "deepl",
    }


def get_supported_languages() -> List[str]:
    """Get list of languages supported by DeepL API."""
    try:
        translator = init_deepl_translator()
        languages = translator.get_target_languages()
        return [lang.code for lang in languages]
    except Exception:
        return SUPPORTED_TARGET_LANGUAGES


if __name__ == "__main__":
    import json

    sample_consent = (
        "By clicking 'Continue', you authorize this application to access your "
        "profile information and email address from the identity provider. "
        "You may revoke this consent at any time in your account settings."
    )

    package = prepare_consent_package(
        consent_id="consent-001",
        source_text=sample_consent,
        provider="okta",
        target_locales=["de-DE", "fr-FR", "es-ES", "ja-JP"],
        source_lang="EN",
    )
    print(json.dumps(package, indent=2))
