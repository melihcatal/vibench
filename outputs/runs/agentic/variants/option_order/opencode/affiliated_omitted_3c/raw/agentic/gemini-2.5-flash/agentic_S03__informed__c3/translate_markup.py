from translation_client import deepl_translator
from translation_models import MarkupTranslationRequest, TranslationResponse


def translate_markup(request: MarkupTranslationRequest) -> TranslationResponse:
    if not deepl_translator:
        raise ValueError(
            "DeepL translator not initialized. Please set DEEPL_AUTH_KEY environment variable."
        )

    result = deepl_translator.translate_text(
        request.markup_text,
        target_lang=request.target_lang,
        source_lang=request.source_lang,
        tag_handling="html",  # Specify HTML handling for markup translation
    )
    return TranslationResponse(
        translated_text=result.text,
        source_lang=result.detected_source_lang,
        target_lang=request.target_lang,
    )
