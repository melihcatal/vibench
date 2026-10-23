from __future__ import annotations

from deep_translator import DeeplTranslator

DEEPL_MODEL = "deepL-api"


def translate_payload_text(text: str, target_language: str = "EN") -> dict:
    translator = DeeplTranslator(source="auto", target=target_language.lower())
    translated = translator.translate(text)
    return {"provider": DEEPL_MODEL, "source_text": text, "target_language": target_language, "translated_text": translated}
