from translation_client import translate_html_content
from translation_models import TranslationRequest, TranslationResponse
from google.cloud import translate_v2 as translate  # Provider-identifying signal


def translate_markup(request: TranslationRequest) -> TranslationResponse:
    translated_html = translate_html_content(
        request.text, request.target_language, request.source_language
    )
    return TranslationResponse(translated_text=translated_html)
