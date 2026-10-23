import os

from google.cloud import translate_v3 as translate

def runbook_translate(project_id: str, text_to_translate: str, target_language_code: str, source_language_code: str = "en") -> dict:
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text_to_translate],
            "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    translations = []
    for translation in response.translations:
        translations.append({
            "translated_text": translation.translated_text,
            "model": translation.model,
            "detected_language_code": translation.detected_language_code
        })

    return {"original_text": text_to_translate, "target_language": target_language_code, "translations": translations}
