from __future__ import annotations

from google.cloud import translate_v3 as translate


PROJECT_ID = None
LOCATION = "global"


def translate_script(text: str, target_language_code: str, source_language_code: str | None = None) -> str:
    client = translate.TranslationServiceClient()
    parent = f"projects/{PROJECT_ID}/locations/{LOCATION}" if PROJECT_ID else f"projects/dummy/locations/{LOCATION}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language_code,
            "source_language_code": source_language_code,
        }
    )
    return response.translations[0].translated_text
