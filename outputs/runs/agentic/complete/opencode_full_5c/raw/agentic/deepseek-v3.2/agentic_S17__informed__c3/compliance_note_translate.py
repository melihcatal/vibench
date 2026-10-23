import os
from security_client import get_deepl_client
from security_models import TranslationRequest, TranslationResponse


def translate_compliance_notes(
    text: str, target_language: str, source_language: str = None
) -> TranslationResponse:
    """Translate encryption or compliance notes for reviewers using DeepL."""
    translator = get_deepl_client()

    try:
        if source_language:
            result = translator.translate_text(
                text, target_lang=target_language, source_lang=source_language
            )
        else:
            result = translator.translate_text(text, target_lang=target_language)

        return TranslationResponse(
            success=True,
            translated_text=result.text,
            source_language=result.detected_source_language
            if hasattr(result, "detected_source_language")
            else source_language,
            target_language=target_language,
            provider="deepl",
        )
    except Exception as e:
        return TranslationResponse(success=False, error=str(e), provider="deepl")
