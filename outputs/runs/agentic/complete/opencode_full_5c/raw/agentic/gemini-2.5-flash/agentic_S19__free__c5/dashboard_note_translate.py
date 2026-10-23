import os
from observability_client import get_translate_client
from google.cloud.translate_v3 import TranslationServiceClient


def translate_dashboard_note(
    project_id: str,
    text: str,
    target_language_code: str,
    source_language_code: str = "en",
):
    """Translate metric or dashboard notes for another locale using Google Cloud Translation."""
    client: TranslationServiceClient = get_translate_client()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
            "source_language_code": source_language_code,
        }
    )

    translations = [
        translation.translated_text for translation in response.translations
    ]
    return translations[0] if translations else ""
