from typing import List, Dict, Any, Optional

class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None

    def __init__(self, text: str, target_language: str, source_language: Optional[str] = None):
        self.text = text
        self.target_language = target_language
        self.source_language = source_language

class TranslationResponse:
    original_text: str
    translated_text: str
    detected_source_language: Optional[str] = None

    def __init__(self, original_text: str, translated_text: str, detected_source_language: Optional[str] = None):
        self.original_text = original_text
        self.translated_text = translated_text
        self.detected_source_language = detected_source_language

class BatchTranslationRequest:
    texts: List[str]
    target_language: str
    source_language: Optional[str] = None

    def __init__(self, texts: List[str], target_language: str, source_language: Optional[str] = None):
        self.texts = texts
        self.target_language = target_language
        self.source_language = source_language

class BatchTranslationResponse:
    original_texts: List[str]
    translated_texts: List[str]
    detected_source_languages: Optional[List[str]] = None

    def __init__(self, original_texts: List[str], translated_texts: List[str], detected_source_languages: Optional[List[str]] = None):
        self.original_texts = original_texts
        self.translated_texts = translated_texts
        self.detected_source_languages = detected_source_languages

class DictionaryTranslationRequest:
    data: Dict[str, Any]
    target_language: str
    source_language: Optional[str] = None

    def __init__(self, data: Dict[str, Any], target_language: str, source_language: Optional[str] = None):
        self.data = data
        self.target_language = target_language
        self.source_language = source_language

class DictionaryTranslationResponse:
    original_data: Dict[str, Any]
    translated_data: Dict[str, Any]

    def __init__(self, original_data: Dict[str, Any], translated_data: Dict[str, Any]):
        self.original_data = original_data
        self.translated_data = translated_data
