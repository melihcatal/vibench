from typing import Dict, Any


class TranslationRequest:
    def __init__(self, text: str, source_lang: str, target_lang: str):
        self.text = text
        self.source_lang = source_lang
        self.target_lang = target_lang


class TranslationResponse:
    def __init__(self, translated_text: str, source_lang: str, target_lang: str):
        self.translated_text = translated_text
        self.source_lang = source_lang
        self.target_lang = target_lang


def normalize_text(text: str) -> str:
    # Placeholder for text normalization logic
    return text.strip().lower()


def create_translation_request(text: str, source_lang: str, target_lang: str) -> TranslationRequest:
    return TranslationRequest(text, source_lang, target_lang)


def create_translation_response(translated_text: str, source_lang: str, target_lang: str) -> TranslationResponse:
    return TranslationResponse(translated_text, source_lang, target_lang)