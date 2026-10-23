from translation_client import translate_text_request
from translation_models import TranslationRequest


def translate_text(text: str, source_language: str, target_language: str):
    return translate_text_request(
        TranslationRequest(text, source_language, target_language)
    ).as_dict()
