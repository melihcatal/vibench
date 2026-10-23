import dataclasses
from typing import List, Dict, Any

@dataclasses.dataclass
class TranslationRequest:
    text: str | List[str]
    source_language: str
    target_language: str
    mime_type: str = "text/plain"

@dataclasses.dataclass
class TranslationResponse:
    translated_text: str | List[str]
    source_language: str
    target_language: str
