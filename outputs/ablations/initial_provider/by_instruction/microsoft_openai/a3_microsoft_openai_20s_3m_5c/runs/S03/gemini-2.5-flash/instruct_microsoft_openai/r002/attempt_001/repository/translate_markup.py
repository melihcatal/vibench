import os
from translation_client import OpenAITranslationClient
from translation_models import MarkupTranslationRequest, TranslationResponse

def translate_markup(markup_text: str, target_language: str, source_language: str = None, markup_type: str = "html") -> TranslationResponse:
    """
    Translates HTML or markup while preserving tags using OpenAI.
    """
    client = OpenAITranslationClient()
    request = MarkupTranslationRequest(
        markup_text=markup_text,
        target_language=target_language,
        source_language=source_language,
        markup_type=markup_type
    )
    response = client.translate_markup(request)
    return response
