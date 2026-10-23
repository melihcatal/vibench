from __future__ import annotations

from typing import Optional

from translation_client import get_google_parent, get_translate_client
from translation_models import TranslationRequest, TranslationResult, normalize_translation_item


TRANSLATION_MODEL = "general/nmt"


def translate_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    project_id: Optional[str] = None,
    location: Optional[str] = None,
) -> TranslationResult:
    client = get_translate_client()
    parent = get_google_parent(project_id=project_id, location=location)
    request = TranslationRequest(
        text=text,
        source_language=source_language,
        target_language=target_language,
        content_type="text/plain",
    )
    response = client.translate_text(
        request={
            "parent": parent,
            **request.as_google_translate_payload(),
            "model": f"projects/{parent.split('/')[1]}/locations/{parent.split('/')[-1]}/models/{TRANSLATION_MODEL}",
        }
    )
    first = response.translations[0]
    return normalize_translation_item(
        {
            "translated_text": first.translated_text,
            "detected_language_code": getattr(first, "detected_language_code", None),
            "model": TRANSLATION_MODEL,
        }
    )
