from __future__ import annotations

from google.cloud import translate_v3 as translate

TARGET_LANGUAGE = "en"


def translate_consent_copy(text: str, target_language: str = TARGET_LANGUAGE) -> dict[str, str]:
    client = translate.TranslationServiceClient()
    parent = "projects/example-project/locations/global"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )
    translated = response.translations[0].translated_text if response.translations else ""
    return {"source_text": text, "translated_text": translated, "target_language": target_language}
