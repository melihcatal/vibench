import os
from google.cloud import translate

def record_translate(text_content: str, target_language: str, project_id: str, config: dict = None):
    config = config or {}
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text_content],
            "target_language_code": target_language,
        }
    )

    translations = []
    for translation in response.translations:
        translations.append({
            "translated_text": translation.translated_text,
            "detected_language_code": translation.detected_language_code
        })
    return {"translations": translations}
