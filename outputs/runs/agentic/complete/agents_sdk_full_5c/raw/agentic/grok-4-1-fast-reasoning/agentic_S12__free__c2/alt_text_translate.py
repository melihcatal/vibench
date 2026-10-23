from typing import Dict, Any
from vision_client import translate_client
from google.cloud import translate_v2 as translate

def alt_text_translate(alt_text: str, target_language: str = 'es') -> str:
    if not alt_text:
        return ''
    result = translate_client.translate(alt_text, target_language=target_language)
    return result['translatedText']
