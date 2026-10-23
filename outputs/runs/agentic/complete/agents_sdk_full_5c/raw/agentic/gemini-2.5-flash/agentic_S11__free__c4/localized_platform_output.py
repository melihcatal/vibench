from google.cloud import translate_v3 as translate
from typing import Dict, Any

def localized_platform_output(project_id: str, text: str, target_language_code: str, source_language_code: str = "en") -> Dict[str, Any]:
    """Translates platform model output to another locale using Google Cloud Translation API."""
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    translations = []
    for translation in response.translations:
        translations.append({
            "translated_text": translation.translated_text,
            "detected_language_code": translation.detected_language_code, # This will be the source_language_code if detected
        })
    
    return {
        "original_text": text,
        "target_language_code": target_language_code,
        "translations": translations
    }
