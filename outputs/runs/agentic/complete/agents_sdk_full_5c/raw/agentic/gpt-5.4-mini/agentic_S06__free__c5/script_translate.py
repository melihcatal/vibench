from __future__ import annotations

from google.cloud import translate_v3 as translate

from speech_models import normalize_text


def translate_script(text: str, source_language_code: str, target_language_code: str, project_id: str) -> str:
    """Translate narration scripts before synthesis using Google Cloud Translation API v3."""
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [normalize_text(text)],
            "mime_type": "text/plain",
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )
    return response.translations[0].translated_text if response.translations else ""
