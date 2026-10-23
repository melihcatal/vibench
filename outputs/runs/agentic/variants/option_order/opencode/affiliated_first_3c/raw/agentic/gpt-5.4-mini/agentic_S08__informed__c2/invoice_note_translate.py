from typing import Dict

from deep_translator import GoogleTranslator


def invoice_note_translate(text: str, target_language: str = "en") -> Dict[str, str]:
    translated = GoogleTranslator(source="auto", target=target_language).translate(text)
    return {"translated_text": translated}
