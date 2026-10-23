from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class TranslationRequest:
    text: str
    source_language_code: str
    target_language_code: str
    text_type: Optional[str] = None # For HTML/Plain text

@dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_language_code: str
    target_language_code: str

@dataclass
class DictionaryTranslationRequest:
    data: Dict[str, Any]
    source_language_code: str
    target_language_code: str

@dataclass
class TranslationResponse:
    translated_text: str
    source_language_code: str
    target_language_code: str

@dataclass
class BatchTranslationResponse:
    translated_texts: List[str]

@dataclass
class DictionaryTranslationResponse:
    translated_data: Dict[str, Any]
