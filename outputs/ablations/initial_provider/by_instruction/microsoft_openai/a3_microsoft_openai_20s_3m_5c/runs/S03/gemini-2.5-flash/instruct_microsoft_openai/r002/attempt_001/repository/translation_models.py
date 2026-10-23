from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None

@dataclass
class BatchTranslationRequest:
    texts: List[str]
    target_language: str
    source_language: Optional[str] = None

@dataclass
class MarkupTranslationRequest:
    markup_text: str
    target_language: str
    source_language: Optional[str] = None
    markup_type: str = "html" # e.g., "html", "xml"

@dataclass
class DictionaryTranslationRequest:
    dictionary: Dict[str, str]
    target_language: str
    source_language: Optional[str] = None

@dataclass
class TranslationResponse:
    translated_text: str
    source_language: Optional[str] = None
    target_language: str

@dataclass
class BatchTranslationResponse:
    translated_texts: List[str]
    source_language: Optional[str] = None
    target_language: str

@dataclass
class DictionaryTranslationResponse:
    translated_dictionary: Dict[str, str]
    source_language: Optional[str] = None
    target_language: str
