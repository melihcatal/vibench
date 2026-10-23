import os
import json
from typing import Dict, Any, List
from google.cloud import translate_v2 as translate


def translate_consent_text(text: str, target_language: str = "en") -> str:
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required"
        )

    if not os.path.exists(credentials_path):
        raise FileNotFoundError(
            f"Google credentials file not found: {credentials_path}"
        )

    try:
        client = translate.Client()

        if isinstance(text, list):
            result = client.translate(
                text, target_language=target_language, format_="text"
            )
            translations = [item["translatedText"] for item in result]
            return translations
        else:
            result = client.translate(
                text, target_language=target_language, format_="text"
            )
            return result["translatedText"]

    except Exception as e:
        raise Exception(f"Google Cloud Translation failed: {e}")


def translate_consent_screen(
    consent_data: Dict[str, Any], target_language: str
) -> Dict[str, Any]:
    translated = {}

    text_fields = [
        "title",
        "description",
        "terms_text",
        "privacy_policy_text",
        "accept_button",
        "decline_button",
        "learn_more_text",
    ]

    for field in text_fields:
        if field in consent_data and consent_data[field]:
            try:
                translated[field] = translate_consent_text(
                    consent_data[field], target_language
                )
            except Exception as e:
                translated[field] = f"Translation failed: {str(e)}"

    for key, value in consent_data.items():
        if key not in translated:
            translated[key] = value

    translated["original_language"] = consent_data.get("language", "en")
    translated["target_language"] = target_language
    translated["translation_service"] = "google_cloud_translation"

    return translated


def detect_consent_language(text: str) -> str:
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required"
        )

    try:
        client = translate.Client()
        result = client.detect_language(text)

        return result["language"]

    except Exception as e:
        raise Exception(f"Language detection failed: {e}")


def batch_translate_consents(
    consents: List[Dict[str, Any]], target_languages: List[str]
) -> Dict[str, List[Dict[str, Any]]]:
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required"
        )

    results = {}

    for lang in target_languages:
        lang_results = []

        for consent in consents:
            try:
                translated = translate_consent_screen(consent, lang)
                lang_results.append(translated)
            except Exception as e:
                lang_results.append(
                    {
                        "error": str(e),
                        "original_consent": consent,
                        "target_language": lang,
                    }
                )

        results[lang] = lang_results

    return results


def get_supported_languages() -> List[Dict[str, str]]:
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required"
        )

    try:
        client = translate.Client()
        languages = client.get_languages()

        return languages

    except Exception as e:
        raise Exception(f"Failed to get supported languages: {e}")


def translate_identity_provider_consent(
    provider_name: str, consent_copy: Dict[str, str], user_locale: str
) -> Dict[str, str]:
    source_language = detect_consent_language(
        list(consent_copy.values())[0] if consent_copy else "en"
    )

    if source_language == user_locale:
        return consent_copy

    translated_copy = {}

    for key, text in consent_copy.items():
        try:
            translated_text = translate_consent_text(text, user_locale)
            translated_copy[key] = translated_text
        except Exception as e:
            translated_copy[key] = f"{text} [Translation failed: {str(e)}]"

    return translated_copy
