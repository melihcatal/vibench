from typing import Dict

from google.cloud import translate_v3 as translate


def dashboard_note_translate(text: str, target_language: str, parent: str) -> Dict[str, str]:
    client = translate.TranslationServiceClient()
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
