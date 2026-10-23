from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from google.cloud import translate_v3 as translate


GOOGLE_TRANSLATE_MODEL = "general/nmt"


def get_google_project_id() -> str:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT or GCLOUD_PROJECT must be set")
    return project_id


def get_google_location() -> str:
    return os.getenv("GOOGLE_TRANSLATE_LOCATION", "global")


def get_translation_parent() -> str:
    return f"projects/{get_google_project_id()}/locations/{get_google_location()}"


def get_translation_client() -> translate.TranslationServiceClient:
    return translate.TranslationServiceClient()


def translate_texts(
    texts: List[str],
    target_language: str,
    source_language: Optional[str] = None,
    mime_type: str = "text/plain",
) -> Dict[str, Any]:
    client = get_translation_client()
    request: Dict[str, Any] = {
        "parent": get_translation_parent(),
        "contents": texts,
        "mime_type": mime_type,
        "target_language_code": target_language,
        "model": GOOGLE_TRANSLATE_MODEL,
    }
    if source_language:
        request["source_language_code"] = source_language
    response = client.translate_text(request=request)
    return {
        "translations": [
            {
                "translatedText": item.translated_text,
                "detectedLanguageCode": item.detected_language_code,
                "model": GOOGLE_TRANSLATE_MODEL,
            }
            for item in response.translations
        ],
        "provider": "google-cloud-translate",
        "model": GOOGLE_TRANSLATE_MODEL,
    }
