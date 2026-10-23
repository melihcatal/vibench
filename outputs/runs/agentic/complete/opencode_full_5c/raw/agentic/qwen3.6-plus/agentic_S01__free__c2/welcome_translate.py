import os
from typing import Optional, Dict, Any, List

from google.cloud import translate_v2 as translate


GOOGLE_CLOUD_PROJECT_ENV = "GOOGLE_CLOUD_PROJECT"
GOOGLE_APPLICATION_CREDENTIALS_ENV = "GOOGLE_APPLICATION_CREDENTIALS"

ONBOARDING_COPY = {
    "welcome_title": "Welcome to Our Platform",
    "welcome_body": "We are thrilled to have you join us. Complete your profile to get started.",
    "next_steps": "Next steps: verify your email, set up your profile, and explore features.",
    "support_message": "Need help? Contact our support team anytime.",
}


def get_client() -> translate.Client:
    return translate.Client()


def translate_onboarding_copy(
    target_language: str,
    custom_copies: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    client = get_client()
    copies = custom_copies or ONBOARDING_COPY

    texts = list(copies.values())
    keys = list(copies.keys())

    result = client.translate(texts, target_language=target_language)

    translated = {}
    if isinstance(result, list):
        for i, key in enumerate(keys):
            translated[key] = result[i]["translatedText"]
    else:
        translated[keys[0]] = result["translatedText"]

    return {
        "target_language": target_language,
        "source_language": "en",
        "translated_copies": translated,
    }


def translate_single_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = "en",
) -> Dict[str, Any]:
    client = get_client()

    result = client.translate(
        text, target_language=target_language, source_language=source_language
    )

    return {
        "original": text,
        "translated": result["translatedText"],
        "detected_source": result.get("detectedSourceLanguage", source_language),
        "target_language": target_language,
    }


def translate_batch(
    texts: List[str],
    target_language: str,
    source_language: Optional[str] = "en",
) -> List[Dict[str, Any]]:
    client = get_client()

    result = client.translate(
        texts, target_language=target_language, source_language=source_language
    )

    outputs = []
    for i, item in enumerate(result):
        outputs.append(
            {
                "index": i,
                "original": texts[i],
                "translated": item["translatedText"],
                "detected_source": item.get("detectedSourceLanguage", source_language),
            }
        )

    return outputs
