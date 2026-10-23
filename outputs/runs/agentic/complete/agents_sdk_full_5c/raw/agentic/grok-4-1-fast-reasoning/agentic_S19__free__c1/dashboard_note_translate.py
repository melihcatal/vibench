from google.cloud import translate_v2 as translate
from typing import Dict, str

def translate_dashboard_note(note: str, target_language: str = 'fr') -> Dict[str, str]:
    client = translate.Client()
    result = client.translate(note, target_language=target_language)
    return {
        "original": note,
        "translated": result['translatedText'],
        "detected_source_language": result['detectedSourceLanguage']
    }
