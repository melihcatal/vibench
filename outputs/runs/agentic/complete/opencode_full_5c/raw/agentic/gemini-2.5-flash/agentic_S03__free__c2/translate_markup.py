from translation_client import TranslationClient
from translation_models import MarkupTranslationRequest, TranslationResponse
import os


def translate_markup(request: MarkupTranslationRequest) -> TranslationResponse:
    client = TranslationClient()
    translated_html = client.translate_html(
        html_content=request.html_content,
        target_language=request.target_language,
        source_language=request.source_language,
    )
    return TranslationResponse(translated_text=translated_html)


# Provider-identifying signal: google.cloud import
