from __future__ import annotations

from deepl import Translator

from messaging_models import TranslationRequest, TranslationResult


def translate_payload(request: TranslationRequest, auth_key: str) -> TranslationResult:
    translator = Translator(auth_key)
    result = translator.translate_text(
        request.text,
        source_lang=request.source_language,
        target_lang=request.target_language,
    )
    return TranslationResult(text=result.text, source_language=request.source_language, target_language=request.target_language)
