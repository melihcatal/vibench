import json
from typing import Dict, Any, Optional
from google.cloud import translate_v2 as translate
from messaging_models import PubSubMessage


def translate_payload(
    msg: PubSubMessage, target_language: str = "es"
) -> Optional[Dict[str, Any]]:
    text = msg.data.get("text")
    if not text:
        return None
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    translated = {
        "original_text": result["input"],
        "translated_text": result["translatedText"],
        "source_language": result["detectedSourceLanguage"],
    }
    return translated
