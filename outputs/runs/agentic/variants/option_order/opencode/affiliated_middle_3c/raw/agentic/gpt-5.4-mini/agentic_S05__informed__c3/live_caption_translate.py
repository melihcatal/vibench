import os

import deepl

from speech_models import normalize_text


def translate_live_caption(text: str, target_language: str = "ES") -> str:
    client = deepl.Translator(os.environ.get("DEEPL_AUTH_KEY", ""))
    result = client.translate_text(normalize_text(text), target_lang=target_language)
    return result.text
