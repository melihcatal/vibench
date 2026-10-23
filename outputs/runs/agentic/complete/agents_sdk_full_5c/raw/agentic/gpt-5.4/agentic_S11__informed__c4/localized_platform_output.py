from __future__ import annotations

from typing import Dict

import deepl


DEFAULT_TARGET_LANG = "DE"


def localized_platform_output(text: str, target_lang: str = DEFAULT_TARGET_LANG) -> Dict[str, str]:
    translator = deepl.Translator(auth_key=__import__("os").environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(text, target_lang=target_lang)
    return {
        "provider": "DeepL API",
        "target_lang": target_lang,
        "translated_text": result.text,
        "detected_source_lang": result.detected_source_lang,
    }
