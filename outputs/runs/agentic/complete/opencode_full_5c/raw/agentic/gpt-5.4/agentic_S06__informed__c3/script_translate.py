from __future__ import annotations

import deepl

from speech_models import TranslationResult, first_text


def translate_script(
    script: str, target_language: str, source_language: str | None = None
) -> TranslationResult:
    translator = deepl.Translator(__import__("os").getenv("DEEPL_AUTH_KEY") or "")
    response = translator.translate_text(
        first_text(script),
        target_lang=target_language.upper(),
        source_lang=source_language.upper() if source_language else None,
        preserve_formatting=True,
    )
    return TranslationResult(
        translated_text=response.text,
        detected_source_language=getattr(
            response, "detected_source_lang", source_language
        ),
        target_language=target_language.upper(),
    )
