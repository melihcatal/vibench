import os
from typing import Dict, Any

import deepl


def translate_with_deepl(
    text: str, target_lang: str = "DE", source_lang: str = "EN"
) -> Dict[str, Any]:
    """
    Translate text using DeepL API.
    """
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))

    try:
        result = translator.translate_text(
            text, target_lang=target_lang, source_lang=source_lang
        )

        return {
            "translated_text": result.text,
            "detected_source_language": result.detected_source_lang,
            "provider": "deepl",
        }
    except Exception as e:
        raise Exception(f"Failed to translate text: {e}")
