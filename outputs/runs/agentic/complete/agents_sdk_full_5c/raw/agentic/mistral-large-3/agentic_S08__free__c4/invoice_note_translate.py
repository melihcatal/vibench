from google.cloud import translate_v2 as translate
from typing import Dict, Any


def translate_invoice_note(text: str, target_language: str = "en") -> Dict[str, Any]:
    client = translate.Client()

    result = client.translate(
        text,
        target_language=target_language,
        model="nmt"
    )

    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"]
    }