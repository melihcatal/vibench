from dataclasses import dataclass
from typing import List, Dict, Any

# These models are local data structures used to standardize the inputs
# and outputs for the translation functions in this project. They are not
# tied to any specific provider's API models.

@dataclass
class SingleTranslation:
    """Represents a request to translate a single string."""
    text: str
    source_language: str
    target_language: str

@dataclass
class BatchTranslation:
    """Represents a request to translate a list of strings."""
    texts: List[str]
    source_language: str
    target_language: str

@dataclass
class TranslationResponse:
    """Represents a normalized response for a single translation."""
    translated_text: str
    detected_source_language: str

@dataclass
class BatchTranslationResponse:
    """Represents a normalized response for a batch translation."""
    translations: List[Dict[str, Any]]
