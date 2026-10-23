import os
from typing import List, Dict, Any
from google.cloud import translate_v3

def translate_segments(segments: List[str], target_language_code: str = "es") -> List[str]:
    """
    Translates a list of text segments using Google Cloud Translation API.
    """
    client = translate_v3.TranslationServiceClient()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
    
    parent = f"projects/{project_id}/locations/global"
    
    if not segments:
        return []

    translations = []
    # The API allows batch translation of multiple texts in one request
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": segments,
            "target_language_code": target_language_code,
            "mime_type": "text/plain",
        }
    )
    
    for translation in response.translations:
        translations.append(translation.translated_text)
            
    return translations
