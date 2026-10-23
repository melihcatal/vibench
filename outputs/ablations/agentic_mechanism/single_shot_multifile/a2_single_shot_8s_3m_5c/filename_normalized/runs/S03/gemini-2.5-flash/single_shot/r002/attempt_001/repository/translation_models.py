from dataclasses import dataclass, field
from typing import Optional, Dict, List

@dataclass
class TranslationRequest:
    text: str
    source_language_code: str
    target_language_code: str
    mime_type: str = "text/plain"

@dataclass
class TranslationResponse:
    translated_text: str
    detected_language_code: Optional[str] = None

@dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_language_code: str
    target_language_code: str
    mime_type: str = "text/plain"

@dataclass
class BatchTranslationResponse:
    translations: List[TranslationResponse]

@dataclass
class DictTranslationRequest:
    dictionary: Dict[str, str]
    source_language_code: str
    target_language_code: str
    mime_type: str = "text/plain"

@dataclass
class DictTranslationResponse:
    translated_dictionary: Dict[str, TranslationResponse]
