from typing import Dict, Any

from observability_client import get_translate_client

def dashboard_note_translate(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, str]:
    config = config or {}
    translate_client = get_translate_client()

    text_to_translate = payload["text_to_translate"]
    target_language = payload["target_language"]

    response = translate_client.translate(
        text_to_translate, target_language=target_language)
    
    translated_text = response["translatedText"]

    return {"translated_text": translated_text}
