import os
from typing import Dict, str, Optional
from deepl import Translator

translator = Translator(os.getenv("DEEPL_AUTH_KEY"))


def translate_payload_text(
    text: str, target_lang: str = "EN"
) -> Optional[Dict[str, str]]:
    if not text:
        return None
    try:
        result = translator.translate_text(text, target_lang=target_lang)
        return {
            "original": text,
            "translated": result.text,
            "detected_source_lang": result.detected_source_lang,
        }
    except Exception:
        return None
