import os
from google.cloud import translate_v2 as translate
from typing import Dict

client = translate.Client()

def translate_payload(text: str, target_language: str = "en") -> Dict[str, str]:
    result = client.translate(
        text,
        target_language=target_language,
        format_="text"
    )
    
    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"]
    }