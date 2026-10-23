import os
from typing import List, Dict
from google.cloud import translate_v2 as translate

def translate_log_messages(log_messages: List[str], target_language: str = 'es') -> List[Dict[str, str]]:
    client = translate.Client()
    translations = []

    for message in log_messages:
        try:
            result = client.translate(
                message,
                target_language=target_language
            )
            translations.append({
                'original_text': message,
                'translated_text': result['translatedText'],
                'detected_source_language': result['detectedSourceLanguage']
            })
        except Exception as e:
            translations.append({
                'original_text': message,
                'error': str(e)
            })
    return translations
