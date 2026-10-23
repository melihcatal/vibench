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

class DictionaryTranslationRequest:
    def __init__(self, dictionary: Dict[str, str], source_language: str, target_language: str):
        self.dictionary = dictionary
        self.source_language = source_language
        self.target_language = target_language

class TranslationResponse:
    def __init__(self, translated_text: str, source_language: str, target_language: str):
        self.translated_text = translated_text
        self.source_language = source_language
        self.target_language = target_language

class BatchTranslationResponse:
    def __init__(self, translated_texts: List[str], source_language: str, target_language: str):
        self.translated_texts = translated_texts
        self.source_language = source_language
        self.target_language = target_language

class DictionaryTranslationResponse:
    def __init__(self, translated_dictionary: Dict[str, str], source_language: str, target_language: str):
        self.translated_dictionary = translated_dictionary
        self.source_language = source_language
        self.target_language = target_language
