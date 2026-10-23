from translation_client import get_client
from translation_models import TranslationRequest


def translate_text(text: str, source_language: str, target_language: str) -> str:
    return get_client().translate_text(TranslationRequest(text=text, source_language=source_language, target_language=target_language)).translated_text
