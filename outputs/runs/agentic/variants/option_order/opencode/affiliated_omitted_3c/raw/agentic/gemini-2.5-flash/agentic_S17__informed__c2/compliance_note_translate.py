from security_client import get_deepl_translator
from security_models import TranslateRequest, TranslateResponse


def translate_compliance_note(request: TranslateRequest) -> TranslateResponse:
    translator = get_deepl_translator()
    result = translator.translate_text(
        request.text, target_lang=request.target_lang, source_lang=request.source_lang
    )
    return TranslateResponse(
        translated_text=result.text,
        source_lang=result.detected_source_lang,
        target_lang=request.target_lang,
    )
