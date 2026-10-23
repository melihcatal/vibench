import os
from google.cloud import translate

def translate_note(text: str, project_id: str, target_language: str = "en") -> dict:
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translations = []
    for translation in response.translations:
        translations.append({"translated_text": translation.translated_text, "detected_language_code": translation.detected_language_code})
    
    return {"translations": translations, "full_response": str(response)}
