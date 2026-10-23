import os
from google.cloud import translate_v2 as translate

def translate_consent_copy(text: str, target_language: str = "es", project_id: str = None) -> str:
    translate_client = translate.Client(project=project_id)
    
    result = translate_client.translate(text, target_language=target_language)
    
    return result['translatedText']
