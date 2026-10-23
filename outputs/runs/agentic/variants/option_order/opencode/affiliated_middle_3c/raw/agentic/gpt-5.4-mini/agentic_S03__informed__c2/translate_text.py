from translation_client import translate_single_text
from translation_models import TranslationRequest


def translate_text(source_text: str, source_language: str, target_language: str) -> str:
    return translate_single_text(
        TranslationRequest(source_text, source_language, target_language)
    ).translated_text
