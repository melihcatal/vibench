from __future__ import annotations

from google.cloud import translate_v3


def translate_consent_copy(text: str, target_language: str = "es") -> str:
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{__import__('os').environ.get('GOOGLE_CLOUD_PROJECT', 'example')}/locations/global"
    response = client.translate_text(
        contents=[text],
        target_language_code=target_language,
        parent=parent,
        mime_type="text/plain",
    )
    return response.translations[0].translated_text if response.translations else ""
