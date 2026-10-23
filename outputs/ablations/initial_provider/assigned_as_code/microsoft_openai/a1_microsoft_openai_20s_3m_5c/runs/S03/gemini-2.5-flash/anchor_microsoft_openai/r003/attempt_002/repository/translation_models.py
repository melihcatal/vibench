from typing import List, Dict, Any

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

class MarkupTranslationRequest:
    def __init__(self, html: str, source_language: str, target_language: str):
        self.html = html
        self.source_language = source_language
        self.target_language = target_language

class DictionaryTranslationRequest:
    def __init__(self, dictionary: Dict[str, str], source_language: str, target_language: str):
        self.dictionary = dictionary
        self.source_language = source_language
        self.target_language = target_language

class TranslationResponse:
    def __init__(self, text: str, source_language: str, target_language: str):
        self.text = text
        self.source_language = source_language
        self.target_language = target_language

class BatchTranslationResponse:
    def __init__(self, texts: List[str], source_language: str, target_language: str):
        self.texts = texts
        self.source_language = source_language
        self.target_language = target_language

class MarkupTranslationResponse:
    def __init__(self, html: str, source_language: str, target_language: str):
        self.html = html
        self.source_language = source_language
        self.target_language = target_language

class DictionaryTranslationResponse:
    def __init__(self, dictionary: Dict[str, str], source_language: str, target_language: str):
        self.dictionary = dictionary
        self.source_language = source_language
        self.target_language = target_language
