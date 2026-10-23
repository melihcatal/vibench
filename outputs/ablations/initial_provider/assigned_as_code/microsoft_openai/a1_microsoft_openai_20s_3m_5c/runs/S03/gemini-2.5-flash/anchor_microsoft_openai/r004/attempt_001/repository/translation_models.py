from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str

@dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_language: str
    target_language: str

@dataclass
class MarkupTranslationRequest:
    html: str
    source_language: str
    target_language: str

@dataclass
class DictionaryTranslationRequest:
    data: Dict[str, str]
    source_language: str
    target_language: str

@dataclass
class TranslationResponse:
    text: str
    source_language: str
    target_language: str

@dataclass
class BatchTranslationResponse:
    texts: List[str]
    source_language: str
    target_language: str

@dataclass
class MarkupTranslationResponse:
    html: str
    source_language: str
    target_language: str

@dataclass
class DictionaryTranslationResponse:
    data: Dict[str, str]
    source_language: str
    target_language: str
