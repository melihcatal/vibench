from typing import Dict, List
from translation_client import GoogleTranslationClient
from translation_models import TranslationRequest, normalize_language_code


def translate_text(text: str, target_language: str, source_language: str = None) -> str:
    client = GoogleTranslationClient()
    target_language = normalize_language_code(target_language)
    source_language = (
        normalize_language_code(source_language) if source_language else None
    )

    request = TranslationRequest(
        text=text, target_language=target_language, source_language=source_language
    )
    response = client.translate_text(request)
    return response.translated_text
