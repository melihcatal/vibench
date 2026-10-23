import os
import deepl


def invoice_note_translate(note: str, target_language: str = "EN") -> str:
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY not set")
    translator = deepl.Translator(api_key)
    result = translator.translate_text(note, target_lang=target_language)
    return result.text
