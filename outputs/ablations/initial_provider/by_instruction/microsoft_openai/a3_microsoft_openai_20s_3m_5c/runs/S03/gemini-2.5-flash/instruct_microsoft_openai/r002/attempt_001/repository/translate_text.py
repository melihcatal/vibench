import os
from translation_client import OpenAITranslationClient
from translation_models import TranslationRequest, TranslationResponse

def translate_text(text: str, target_language: str, source_language: str = None) -> TranslationResponse:
    """
    Translates a single text string between languages using OpenAI.
    """
    client = OpenAITranslationClient()
    request = TranslationRequest(text=text, target_language=target_language, source_language=source_language)
    response = client.translate_text(request)
    return response
