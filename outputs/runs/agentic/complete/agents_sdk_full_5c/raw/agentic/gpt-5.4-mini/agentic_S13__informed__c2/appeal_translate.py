from __future__ import annotations

from deepl import Translator

from safety_models import TranslationResult


translator = Translator(auth_key="DEEPL_AUTH_KEY")


def appeal_translate(text: str, target_language: str = "EN-US") -> TranslationResult:
    result = translator.translate_text(text, target_lang=target_language)
    return TranslationResult(
        translated_text=result.text,
        source_language=getattr(result, "detected_source_lang", None),
        target_language=target_language,
        provider="DeepL",
    )
