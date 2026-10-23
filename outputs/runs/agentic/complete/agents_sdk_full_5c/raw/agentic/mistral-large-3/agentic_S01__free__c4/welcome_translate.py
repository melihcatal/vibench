from google.cloud import translate_v2 as translate
from typing import Dict, Any


def translate_welcome_message(text: str, target_language: str) -> str:
    client = translate.Client()
    
    result = client.translate(
        text,
        target_language=target_language,
        model="nmt"
    )
    
    return result["translatedText"]