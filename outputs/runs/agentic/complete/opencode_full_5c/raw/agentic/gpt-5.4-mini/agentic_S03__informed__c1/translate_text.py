from translation_client import get_target_language_code, get_translator
from translation_models import TranslationRequest, TranslationResult


def translate_text(
    text: str, source_language: str, target_language: str
) -> TranslationResult:
    request = TranslationRequest(
        text=text, source_language=source_language, target_language=target_language
    )
    translator = get_translator()
    translated = translator.translate_text(
        request.text,
        source_lang=request.source_language,
        target_lang=get_target_language_code(request.target_language),
    )
    return TranslationResult(
        translated_text=str(translated.text),
        source_language=request.source_language,
        target_language=request.target_language,
    )
