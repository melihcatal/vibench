from google.cloud import translate_v2 as translate
from typing import Optional

def translate_compliance_note(note: str, target_language: str = 'es') -> str:
    client = translate.Client()
    result = client.translate(
        note,
        target_language=target_language
    )
    return result['translatedText']