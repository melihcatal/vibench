import os
from typing import Dict, Any, List
from google.cloud import translate_v2 as translate
from database_models import Document

def record_translate(document: Document, target_language_code: str = "es") -> Dict[str, Any]:
    """
    Translates user-facing document fields (title and content) using Google Cloud Translation API.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
    
    translate_client = translate.Client(project=project_id)

    texts_to_translate = [document.title, document.content]
    
    translations = translate_client.translate(
        texts_to_translate,
        target_language=target_language_code
    )

    translated_title = translations[0]["translatedText"]
    translated_content = translations[1]["translatedText"]

    return {
        "original_id": document.id,
        "original_title": document.title,
        "original_content": document.content,
        "translated_title": translated_title,
        "translated_content": translated_content,
        "target_language": target_language_code,
        "source_language_title": translations[0]["detectedSourceLanguage"],
        "source_language_content": translations[1]["detectedSourceLanguage"]
    }
