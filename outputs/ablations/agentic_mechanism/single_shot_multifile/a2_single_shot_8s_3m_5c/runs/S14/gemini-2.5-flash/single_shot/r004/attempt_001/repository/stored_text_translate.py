import os
from google.cloud import translate
from typing import Optional

def translate_stored_text(
    text: str,
    target_language_code: str = 'en',
    source_language_code: Optional[str] = None
) -> dict:
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
    if not project_id:
        return {"status": "error", "message": "GOOGLE_CLOUD_PROJECT_ID environment variable not set."}
    
    client = translate.TranslationServiceClient()
    location = 'global'
    parent = f"projects/{project_id}/locations/{location}"

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language_code,
                "source_language_code": source_language_code,
                "mime_type": "text/plain",
            }
        )

        translations = response.translations
        if translations:
            first_translation = translations[0]
            return {
                "status": "success",
                "translated_text": first_translation.translated_text,
                "detected_source_language": first_translation.detected_language_code,
                "target_language": target_language_code
            }
        else:
            return {"status": "error", "message": "No translation found."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
