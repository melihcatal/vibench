from dataclasses import dataclass, field
from typing import List, Optional, Dict

@dataclass
class TranslationRequest:
    contents: List[str]
    target_language_code: str
    source_language_code: Optional[str] = None
    mime_type: str = "text/plain"

@dataclass
class TranslationResponseItem:
    translated_text: str
    detected_source_language_code: Optional[str] = None

@dataclass
class TranslationResponse:
    translations: List[TranslationResponseItem]

@dataclass
class DictionaryTranslationRequest:
    dictionary: Dict[str, str]
    target_language_code: str
    source_language_code: Optional[str] = None

@dataclass
class DictionaryTranslationResponse:
    translated_dictionary: Dict[str, str]
