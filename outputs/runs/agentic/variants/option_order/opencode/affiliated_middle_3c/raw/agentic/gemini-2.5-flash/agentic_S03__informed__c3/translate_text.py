from translation_client import get_deepl_translator
from translation_models import TranslationRequest, TranslationResponse


def translate_single_text(request: TranslationRequest) -> TranslationResponse:
    translator = get_deepl_translator()
    result = translator.translate_text(
        request.text, target_lang=request.target_lang, source_lang=request.source_lang
    )
    return TranslationResponse(
        translated_text=result.text, detected_source_lang=result.detected_source_lang
    )
