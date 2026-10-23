from google.cloud import translate_v2 as translate
from typing import Dict, Any

def dashboard_note_translate(
    text: str,
    target_language: str = "fr"
) -> Dict[str, Any]:
    client = translate.Client()
    result = client.translate(
        text,
        target_language=target_language
    )
    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"]
    }