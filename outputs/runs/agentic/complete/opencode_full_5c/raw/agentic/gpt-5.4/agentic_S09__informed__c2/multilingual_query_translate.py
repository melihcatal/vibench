from __future__ import annotations

import deepl


def multilingual_query_translate(
    text: str, target_language: str = "EN-US"
) -> dict[str, str]:
    translator = deepl.Translator(__import__("os").environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(text, target_lang=target_language)
    return {
        "source_language": result.detected_source_lang,
        "target_language": target_language,
        "translated_text": result.text,
    }
