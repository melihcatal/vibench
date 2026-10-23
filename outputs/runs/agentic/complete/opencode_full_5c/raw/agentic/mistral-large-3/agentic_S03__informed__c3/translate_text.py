from typing import Optional
from translation_client import DeepLTranslationClient
from translation_models import TranslationRequest


def translate_text(
    text: str, target_language: str, source_language: Optional[str] = None
) -> str:
    """
    Translates a single text string between languages using DeepL API.
    """
    client = DeepLTranslationClient()
    request = TranslationRequest(
        text=text, target_language=target_language, source_language=source_language
    )
    response = client.translate_text(request)
    return response.translated_text
