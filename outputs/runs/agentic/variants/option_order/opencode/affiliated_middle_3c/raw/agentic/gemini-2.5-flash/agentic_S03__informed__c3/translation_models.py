import dataclasses
from typing import List, Dict, Any, Optional


@dataclasses.dataclass
class TranslationRequest:
    text: str | List[str]
    target_lang: str
    source_lang: Optional[str] = None
    tag_handling: Optional[str] = None


@dataclasses.dataclass
class TranslationResponse:
    translated_text: str | List[str]
    detected_source_lang: Optional[str] = None
