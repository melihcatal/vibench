from __future__ import annotations

from google.cloud import translate_v3 as translate

from observability_client import load_config
from observability_models import TranslationResult


def dashboard_note_translate(text: str, target_language: str) -> dict:
    config = load_config()
    client = translate.TranslationServiceClient()
    parent = f"projects/{config.project_id}/locations/{config.translate_location}"
    response = client.translate_text(
        request={"parent": parent, "contents": [text], "mime_type": "text/plain", "target_language_code": target_language}
    )
    translated = response.translations[0].translated_text if response.translations else ""
    result = TranslationResult(text, translated, "auto", target_language)
    return result.__dict__
