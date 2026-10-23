from __future__ import annotations

import os
from typing import Optional

from google.cloud import translate_v3 as translate

from observability_models import NormalizedTextResult


def dashboard_note_translate(text: str, target_language: str, source_language: Optional[str] = None) -> NormalizedTextResult:
    client = translate.TranslationServiceClient()
    parent = f"projects/{os.environ['GOOGLE_CLOUD_PROJECT']}/locations/global"
    response = client.translate_text(
        contents=[text],
        target_language_code=target_language,
        parent=parent,
        source_language_code=source_language or "",
        mime_type="text/plain",
    )
    translated = response.translations[0].translated_text if response.translations else text
    return NormalizedTextResult(text=translated, language=target_language, metadata={"provider": "google-cloud-translate"})
