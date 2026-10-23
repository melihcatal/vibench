from translation_client import TranslationClient
from translation_models import MarkupTranslationRequest, MarkupTranslationResponse

def translate_markup(request: MarkupTranslationRequest) -> MarkupTranslationResponse:
    client_helper = TranslationClient()
    client = client_helper.get_client()
    client_helper.validate_languages(request.source_lang, request.target_lang)

    result = client.translate_text(
        request.markup,
        source_lang=request.source_lang,
        target_lang=request.target_lang,
        tag_handling=request.tag_handling,
        ignore_tags=request.ignore_tags
    )
    return MarkupTranslationResponse(translated_markup=result.text)