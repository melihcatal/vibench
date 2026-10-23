from typing import Any, Dict

from deep_translator import GoogleTranslator


def translate_payload(text: str, target_language: str = "en") -> Dict[str, Any]:
    translated = GoogleTranslator(source="auto", target=target_language).translate(text)
    return {"translated_text": translated, "target_language": target_language, "provider": "google_translate"}
