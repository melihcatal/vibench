from __future__ import annotations

import deepl


def translate_log_message(
    text: str, target_lang: str, source_lang: str | None = None
) -> dict:
    translator = deepl.Translator()
    result = translator.translate_text(
        text, target_lang=target_lang, source_lang=source_lang
    )
    return {
        "provider": "DeepL",
        "detected_source_language": result.detected_source_lang,
        "target_language": target_lang,
        "translated_text": result.text,
    }
