from dataclasses import dataclass
from typing import Any

class TranslationRequest:
    """Model for a single translation request."""
    text: str
    source_lang: str = 'en'
    target_lang: str = 'es'
    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> 'TranslationRequest':
        return cls(**d)

class TranslationResponse:
    """Model for a single translation response."""
    translated_text: str
    def __str__(self) -> str:
        return self.translated_text
    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> 'TranslationResponse':
        return cls(**d)

@dataclass
class TranslationBatchRequest(list):
    """Batch wrapper around TranslationRequest objects."""
    pass  # In practice this mirrors the provider's batch endpoint signature

@dataclass
class TranslationBatchResponse(list):
    """Batch wrapper around TranslationResponse objects."""
    pass
