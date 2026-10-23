import os
import deepl
from typing import Optional


def translate_text(
    text: str, target_lang: str = "EN", source_lang: Optional[str] = None
) -> str:
    """
    Translate generated model output using DeepL API.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(
            text, target_lang=target_lang, source_lang=source_lang
        )
        return result.text
    except deepl.DeepLException as e:
        raise RuntimeError(f"DeepL translation failed: {e}")

    # Map language codes to DeepL format if needed
    lang_map = {
        "en": "EN",
        "es": "ES",
        "fr": "FR",
        "de": "DE",
        "it": "IT",
        "ja": "JA",
        "zh": "ZH",
    }

    target_lang = lang_map.get(target_lang.lower(), target_lang.upper())

    if source_lang:
        source_lang = lang_map.get(source_lang.lower(), source_lang.upper())

    return result.text
