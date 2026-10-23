from __future__ import annotations

import os
from typing import Any

import deepl


DEFAULT_TARGET_LANG = "DE"


def localized_platform_output(text: str, target_lang: str = DEFAULT_TARGET_LANG) -> dict[str, Any]:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(text, target_lang=target_lang)
    return {
        "translated_text": result.text,
        "detected_source_language": result.detected_source_lang,
        "target_language": target_lang,
        "provider_response": result,
    }
