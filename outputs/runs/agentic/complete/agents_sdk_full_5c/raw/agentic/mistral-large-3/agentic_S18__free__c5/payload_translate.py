import os
from google.cloud import translate_v2 as translate
from typing import Dict

client = translate.Client()
TARGET_LANGUAGE = os.getenv("TRANSLATE_TARGET_LANGUAGE", "es")

def translate_payload(payload: Dict) -> Dict:
    text = str(payload)
    result = client.translate(text, target_language=TARGET_LANGUAGE)
    
    return {
        "original": payload,
        "translated_text": result["translatedText"],
        "detected_language": result["detectedSourceLanguage"]
    }