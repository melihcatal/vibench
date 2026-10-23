from translation_client import TranslationClient
from translation_models import TranslationRequest
import os


def translate_text(text: str, target_language: str, source_language: str = None) -> str:
    """
    Translates a single text string using Google Cloud Translation API.
    """
    client = TranslationClient(os.getenv("GOOGLE_CLOUD_PROJECT_ID"))
    request = TranslationRequest(
        text=text, target_language=target_language, source_language=source_language
    )
    return client.translate_text(
        request.text, request.target_language, request.source_language
    )
