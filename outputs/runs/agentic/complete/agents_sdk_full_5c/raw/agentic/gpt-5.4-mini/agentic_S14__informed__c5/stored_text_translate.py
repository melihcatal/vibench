from __future__ import annotations

import os

from google.cloud import translate_v3 as translate

from storage_models import TranslationResult, normalize_text


TRANSLATE_PROJECT_ENV = "GOOGLE_CLOUD_PROJECT"
TRANSLATE_LOCATION_ENV = "GOOGLE_TRANSLATE_LOCATION"


def translate_stored_text(text: str, target_language: str = "en", source_language: str | None = None) -> TranslationResult:
    project_id = os.getenv(TRANSLATE_PROJECT_ENV)
    location = os.getenv(TRANSLATE_LOCATION_ENV, "global")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT is required")
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/{location}"
    request = {"parent": parent, "contents": [normalize_text(text)], "target_language_code": target_language}
    if source_language:
        request["source_language_code"] = source_language
    response = client.translate_text(request=request)
    translated = response.translations[0].translated_text if response.translations else ""
    return TranslationResult(text=translated, raw=response)
