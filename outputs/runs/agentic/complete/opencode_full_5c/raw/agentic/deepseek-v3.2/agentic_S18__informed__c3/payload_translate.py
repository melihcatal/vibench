import os
import json
from typing import Dict, Any, Optional
import deepl


def translate_message_payload(text: str, target_lang: str = "EN") -> Dict[str, Any]:
    """Translate customer-facing message payload text using DeepL API."""
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(text, target_lang=target_lang)

        return {
            "original_text": text,
            "translated_text": result.text,
            "target_language": target_lang,
            "detected_source_language": result.detected_source_language,
            "provider": "DeepL",
            "character_count": len(text),
            "translation_confidence": "high",
        }
    except deepl.DeepLException as e:
        return {
            "error": str(e),
            "provider": "DeepL",
            "original_text": text,
            "target_language": target_lang,
        }
    except Exception as e:
        return {
            "error": str(e),
            "provider": "DeepL",
            "api_auth_key_env": "DEEPL_AUTH_KEY",
        }
