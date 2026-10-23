import os
import deepl
from typing import Dict, Any


def record_translate(
    document: Dict[str, Any], target_lang: str = "en"
) -> Dict[str, Any]:
    deepl_auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not deepl_auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(deepl_auth_key)

    text_to_translate = document.get("content", {}).get("text", "")
    if not text_to_translate:
        return {"translated_text": "", "source_lang": ""}

    result = translator.translate_text(text_to_translate, target_lang=target_lang)
    return {"translated_text": result.text, "source_lang": result.detected_source_lang}
