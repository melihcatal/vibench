from translation_client import TranslationClient
from translation_models import TranslationRequest, TranslationResponse

def translate_text(request: TranslationRequest) -> TranslationResponse:
    client_helper = TranslationClient()
    client = client_helper.get_client()
    client_helper.validate_languages(request.source_lang, request.target_lang)

    result = client.translate_text(
        request.text,
        source_lang=request.source_lang,
        target_lang=request.target_lang
    )
    return TranslationResponse(translated_text=result.text)