from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).split())


@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str

    def normalized(self) -> "TranslationRequest":
        return TranslationRequest(
            text=normalize_text(self.text),
            source_language=normalize_text(self.source_language),
            target_language=normalize_text(self.target_language),
        )


@dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_language: str
    target_language: str


@dataclass
class TranslationResult:
    translated_text: str
    detected_source_language: Optional[str] = None
    provider_metadata: Optional[Dict[str, Any]] = None
