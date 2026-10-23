from typing import Dict, List


class TranslationRequest:
    def __init__(self, source_text: str, source_language: str, target_language: str):
        self.source_text = source_text
        self.source_language = source_language
        self.target_language = target_language


class TranslationResponse:
    def __init__(self, translated_text: str):
        self.translated_text = translated_text


class BatchTranslationRequest:
    def __init__(self, texts: List[str], source_language: str, target_language: str):
        self.texts = texts
        self.source_language = source_language
        self.target_language = target_language


class BatchTranslationResponse:
    def __init__(self, translated_texts: List[str]):
        self.translated_texts = translated_texts


class DictionaryTranslationRequest:
    def __init__(
        self, dictionary: Dict[str, str], source_language: str, target_language: str
    ):
        self.dictionary = dictionary
        self.source_language = source_language
        self.target_language = target_language


class DictionaryTranslationResponse:
    def __init__(self, translated_dictionary: Dict[str, str]):
        self.translated_dictionary = translated_dictionary
