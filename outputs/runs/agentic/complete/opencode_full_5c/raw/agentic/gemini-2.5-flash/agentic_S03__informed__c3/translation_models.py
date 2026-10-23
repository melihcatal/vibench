from typing import List, Dict, Any


class TranslationRequest:
    def __init__(
        self,
        text: str,
        target_language: str,
        source_language: str = None,
        mime_type: str = "text/plain",
    ):
        self.text = text
        self.target_language = target_language
        self.source_language = source_language
        self.mime_type = mime_type


class BatchTranslationRequest:
    def __init__(
        self,
        texts: List[str],
        target_language: str,
        source_language: str = None,
        mime_type: str = "text/plain",
    ):
        self.texts = texts
        self.target_language = target_language
        self.source_language = source_language
        self.mime_type = mime_type


class DictionaryTranslationRequest:
    def __init__(
        self,
        dictionary: Dict[str, str],
        target_language: str,
        source_language: str = None,
        mime_type: str = "text/plain",
    ):
        self.dictionary = dictionary
        self.target_language = target_language
        self.source_language = source_language
        self.mime_type = mime_type


class TranslationResponse:
    def __init__(self, translated_text: str, detected_source_language: str = None):
        self.translated_text = translated_text
        self.detected_source_language = detected_source_language


class BatchTranslationResponse:
    def __init__(
        self, translated_texts: List[str], detected_source_languages: List[str] = None
    ):
        self.translated_texts = translated_texts
        self.detected_source_languages = detected_source_languages


class DictionaryTranslationResponse:
    def __init__(
        self,
        translated_dictionary: Dict[str, str],
        detected_source_languages: Dict[str, str] = None,
    ):
        self.translated_dictionary = translated_dictionary
        self.detected_source_languages = detected_source_languages
