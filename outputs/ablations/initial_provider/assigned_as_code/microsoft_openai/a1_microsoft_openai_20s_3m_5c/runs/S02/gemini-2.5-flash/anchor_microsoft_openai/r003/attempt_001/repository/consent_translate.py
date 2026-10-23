import os
from google.cloud import translate

def translate_consent_copy(text: str, target_language_code: str, project_id: str) -> str:
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Can be "text/plain" or "text/html"
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    
    return translated_text
