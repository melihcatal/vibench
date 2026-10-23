from translation_client import get_translate_client
from translation_models import (
    TranslationRequest,
    TranslationResponse,
    normalize_response,
)


def translate_markup(markup, source_lang, target_lang):
    client = get_translate_client()
    request = TranslationRequest(markup, source_lang, target_lang)
    response = client.translate_text(
        Text=request.text,
        SourceLanguageCode=request.source_lang,
        TargetLanguageCode=request.target_lang,
    )
    return normalize_response(response).translated_text
