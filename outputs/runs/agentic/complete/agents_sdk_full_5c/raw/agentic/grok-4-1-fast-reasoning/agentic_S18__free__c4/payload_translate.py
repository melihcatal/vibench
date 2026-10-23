from google.cloud import translate_v2 as translate
from typing import Optional

def translate_payload(payload: str, target_language: Optional[str] = 'en') -> str:
    client = translate.Client()
    result = client.translate(
        payload,
        target_language=target_language
    )
    return result['translatedText']