from typing import Dict, Any
import os
from deepl import Translator


def localized_platform_output(text: str, target_lang: str) -> Dict[str, Any]:
    """
    Translates text to a target language using DeepL API.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set")

    try:
        translator = Translator(auth_key=auth_key)
        result = translator.translate_text(text, target_lang=target_lang)

        return {
            "provider": "deepl",
            "translated_text": result.text,
            "detected_source_language": result.detected_source_lang,
            "target_language": target_lang,
        }
    except Exception as e:
        raise RuntimeError(f"DeepL translation failed: {str(e)}")
