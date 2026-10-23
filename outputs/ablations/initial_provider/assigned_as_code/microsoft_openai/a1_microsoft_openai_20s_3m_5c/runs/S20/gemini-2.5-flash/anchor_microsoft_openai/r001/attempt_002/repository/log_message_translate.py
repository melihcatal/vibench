import os
from typing import List, Dict, Any
from google.cloud import translate_v2 as translate

def log_message_translate(log_messages: List[str], target_language: str, project_id: str) -> List[Dict[str, str]]:
    translate_client = translate.Client(project=project_id)

    translations = []
    for message in log_messages:
        result = translate_client.translate(message, target_language=target_language)
        translations.append({
            "original_message": message,
            "translated_message": result['translatedText'],
            "detected_source_language": result['detectedSourceLanguage']
        })
    return translations
