from google.cloud import translate_v2 as translate
from typing import List, Dict, Any

def translate_text(text: str, target_language: str) -> Dict[str, Any]:
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return {
        "translated_text": result["translatedText"],
        "source_language": result["detectedSourceLanguage"],
        "target_language": target_language,
    }
