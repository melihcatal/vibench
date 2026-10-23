import os
from google.cloud import translate_v3 as translate

def translate_message_payload(text_content: str, target_language: str, project_id: str) -> dict:
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    try:
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
    except Exception as e:
        raise RuntimeError(f"Failed to translate message payload with Google Cloud Translation: {e}")
