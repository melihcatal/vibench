from __future__ import annotations

from deep_translator import DeeplTranslator


DEEPL_MODEL_NAME = "DeepL API"


def invoice_note_translate(text: str, target_language: str = "EN") -> str:
    translator = DeeplTranslator(api_key=None, source="auto", target=target_language.lower())
    return translator.translate(text)
