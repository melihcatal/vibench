from __future__ import annotations

import os

import deepl


def localized_platform_output(text: str, target_lang: str) -> dict[str, str]:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(text, target_lang=target_lang)
    return {
        "provider": "DeepL API",
        "target_lang": target_lang,
        "text": result.text,
        "detected_source_lang": result.detected_source_lang,
    }
