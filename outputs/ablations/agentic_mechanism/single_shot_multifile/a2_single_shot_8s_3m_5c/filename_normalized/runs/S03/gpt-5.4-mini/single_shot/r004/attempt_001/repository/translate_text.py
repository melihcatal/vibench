import os
from translation_client import get_translation_client
from translation_models import normalize_text_response, TextTranslationRequest, TextTranslationResult


def translate_text(text: str, source_language: str, target_language: str, model: str = "gpt-4.1-mini") -> TextTranslationResult:
    client = get_translation_client()
    request = TextTranslationRequest(text=text, source_language=source_language, target_language=target_language)
    response = client.translate_text(request=request, model=model)
    return normalize_text_response(response)
