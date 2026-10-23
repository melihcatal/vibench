from __future__ import annotations

from google.cloud import translate_v3 as translate

from messaging_models import TranslationResult


def translate_payload_text(text: str, target_language: str = "es") -> TranslationResult:
    client = translate.TranslationServiceClient()
    parent = f"projects/{client.project_path.split('/')[-1] if hasattr(client, 'project_path') else 'demo-project'}/locations/global"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )
    translated = response.translations[0].translated_text if response.translations else text
    return TranslationResult(text=translated, target_language=target_language)
