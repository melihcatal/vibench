from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str

@dataclass
class TranslationResponse:
    translated_text: str
    detected_language: str

@dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_language: str
    target_language: str

@dataclass
class BatchTranslationResponse:
    translated_texts: List[str]
    detected_languages: List[str] # Or a single detected language if all are same

@dataclass
class MarkupTranslationRequest:
    markup_content: str
    source_language: str
    target_language: str

@dataclass
class MarkupTranslationResponse:
    translated_markup_content: str
    detected_language: str

@dataclass
class DictionaryTranslationRequest:
    dictionary: Dict[str, str]
    source_language: str
    target_language: str

@dataclass
class DictionaryTranslationResponse:
    translated_dictionary: Dict[str, str]
    detected_language: str
