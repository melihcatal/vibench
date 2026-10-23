
from typing import Dict, List, Any

class TranslationRequest:
    def __init__(self, text: str, source_language: str, target_language: str):
        self.text = text
        self.source_language = source_language
        self.target_language = target_language

class BatchTranslationRequest:
    def __init__(self, texts: List[str], source_language: str, target_language: str):
        self.texts = texts
        self.source_language = source_language
        self.target_language = target_language

class TranslationResponse:
    def __init__(self, translated_text: str, detected_language: str = None):
        self.translated_text = translated_text
        self.detected_language = detected_language

class BatchTranslationResponse:
    def __init__(self, translated_texts: List[str], detected_languages: List[str] = None):
        self.translated_texts = translated_texts
        self.detected_languages = detected_languages

class MarkupTranslationRequest:
    def __init__(self, markup_text: str, source_language: str, target_language: str):
        self.markup_text = markup_text
        self.source_language = source_language
        self.target_language = target_language

class DictionaryTranslationRequest:
    def __init__(self, dictionary: Dict[str, str], source_language: str, target_language: str):
        self.dictionary = dictionary
        self.source_language = source_language
        self.target_language = target_language
