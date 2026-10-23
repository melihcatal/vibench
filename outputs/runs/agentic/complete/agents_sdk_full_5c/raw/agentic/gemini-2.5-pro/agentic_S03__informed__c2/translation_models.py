from dataclasses import dataclass
from typing import List, Optional

@dataclass
class TranslationRequest:
    """Represents a request for a single text translation."""
    text: str
    target_language: str
    source_language: Optional[str] = None

@dataclass
class TranslationResponse:
    """Represents a response for a single text translation."""
    translated_text: str
    detected_source_language: Optional[str] = None
    original_text: Optional[str] = None

@dataclass
class BatchTranslationResponse:
    """Represents a response for a batch text translation."""
    translations: List[TranslationResponse]

@dataclass
class DictionaryTranslationResponse:
    """Represents a response for a dictionary value translation."""
    translated_dictionary: dict[str, str]
    detected_source_language: Optional[str] = None
