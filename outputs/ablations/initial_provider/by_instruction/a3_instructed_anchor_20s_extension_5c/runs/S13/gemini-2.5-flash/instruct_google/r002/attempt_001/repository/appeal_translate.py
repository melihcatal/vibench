from google.cloud import translate_v3
from typing import Dict, Any

def translate_appeal_text(text_content: str, target_language_code: str, project_id: str) -> Dict[str, Any]:
    translate_client = translate_v3.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    try:
        response = translate_client.translate_text(
            request={
                "parent": parent,
                "contents": [text_content],
                "target_language_code": target_language_code
            }
        )

        translated_text = ""
        if response.translations:
            translated_text = response.translations[0].translated_text

        return {
            "original_text": text_content,
            "translated_text": translated_text,
            "target_language": target_language_code,
            "provider": "Google Cloud Translation API"
        }
    except Exception as e:
        return {
            "error": str(e),
            "provider": "Google Cloud Translation API"
        }

