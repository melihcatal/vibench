from typing import List, Optional
from google.cloud import translate_v3

class TranslationRequest:
    def __init__(self, text: str, source_language_code: str, target_language_code: str):
        self.text = text
        self.source_language_code = source_language_code
        self.target_language_code = target_language_code

class TranslationResponse:
    def __init__(self, translated_text: str):
        self.translated_text = translated_text

class TranslationNormalizer:
    def normalize_before_translation(self, text: str) -> str:
        return text

    def normalize_after_translation(self, text: str) -> str:
        return text