import dataclasses
from typing import List, Dict, Any

@dataclasses.dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str

@dataclasses.dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_language: str
    target_language: str

@dataclasses.dataclass
class MarkupTranslationRequest:
    markup_text: str
    source_language: str
    target_language: str

@dataclasses.dataclass
class DictionaryTranslationRequest:
    dictionary: Dict[str, str]
    source_language: str
    target_language: str

@dataclasses.dataclass
class TranslationResponse:
    text: str
    source_language: str
    target_language: str

@dataclasses.dataclass
class BatchTranslationResponse:
    translations: List[str]
    source_language: str
    target_language: str

@dataclasses.dataclass
class DictionaryTranslationResponse:
    translated_dictionary: Dict[str, str]
    source_language: str
    target_language: str
