"""
Translate onboarding copy into the user's locale using Google Cloud Translation API.

This module uses the google-cloud-translate SDK (Vertex AI / Cloud Translation API)
to translate a set of onboarding messages into the target user locale.

Provider-identifying signals:
  - google.cloud.translate_v2 SDK import
  - TranslateClient from google.cloud.translate_v2
  - GOOGLE_APPLICATION_CREDENTIALS / google-cloud-translate project usage
"""

from __future__ import annotations

import os
from typing import Dict, List, Optional

from google.cloud import translate_v2 as translate


_ONBOARDING_COPY = {
    "welcome_title": "Welcome to our platform!",
    "welcome_body": "Get started by completing your profile and exploring the features.",
    "next_steps": "Next steps: verify your email, set up two-factor authentication, and invite your team.",
    "support_message": "Need help? Contact our support team anytime.",
}


def _get_translation_client() -> translate.Client:
    """Create a Google Cloud Translation v2 client."""
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_path:
        return translate.Client.from_service_account_json(credentials_path)
    return translate.Client()


def welcome_translate(
    target_locale: str = "en",
    source_locale: str = "en",
    custom_copy: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    """
    Translate onboarding copy into the user's preferred locale.

    Uses the Google Cloud Translation API (v2) via google.cloud.translate_v2.

    Args:
        target_locale: ISO 639-1 language code for the target locale.
        source_locale: ISO 639-1 language code for the source locale.
        custom_copy: Optional dict of custom key-value pairs to translate.

    Returns:
        Dict mapping copy keys to translated values.
    """
    copy_to_translate = custom_copy or _ONBOARDING_COPY

    if target_locale == source_locale:
        return dict(copy_to_translate)

    client = _get_translation_client()

    texts = list(copy_to_translate.values())
    keys = list(copy_to_translate.keys())

    result = client.translate(
        texts,
        target_language=target_locale,
        source_language=source_locale,
    )

    translated: Dict[str, str] = {}
    if isinstance(result, list):
        for i, key in enumerate(keys):
            translated[key] = result[i]["translatedText"]
    elif isinstance(result, dict) and "translatedText" in result:
        translated[keys[0]] = result["translatedText"]
    else:
        translated = dict(copy_to_translate)

    return translated


if __name__ == "__main__":
    os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", "service-account.json")

    result = welcome_translate(target_locale="es")
    for key, value in result.items():
        print(f"{key}: {value}")
