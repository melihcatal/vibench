import os
from google.cloud import translate_v2 as translate
from typing import Dict, Any


def translate_consent_text(
    consent_text: str, target_language: str = "en"
) -> Dict[str, Any]:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get(
        "GOOGLE_TRANSLATE_CREDENTIALS", ""
    )

    translate_client = translate.Client()

    result = translate_client.translate(
        consent_text, target_language=target_language, format_="text"
    )

    return {
        "original_text": consent_text,
        "translated_text": result["translatedText"],
        "detected_language": result.get("detectedSourceLanguage", "unknown"),
        "target_language": target_language,
        "provider": "google_translate",
    }


def translate_consent_for_provider(
    provider_consent: Dict[str, str], target_language: str = "en"
) -> Dict[str, Any]:
    translations = {}

    for key, text in provider_consent.items():
        if key in ["title", "description", "terms", "privacy_policy"]:
            translation_result = translate_consent_text(text, target_language)
            translations[key] = translation_result

    return {
        "provider": provider_consent.get("provider", "unknown"),
        "target_language": target_language,
        "translations": translations,
        "all_translated": len(translations)
        == len(
            [
                k
                for k in provider_consent.keys()
                if k in ["title", "description", "terms", "privacy_policy"]
            ]
        ),
    }
