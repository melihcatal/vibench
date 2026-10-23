from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str


@dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_language: str
    target_language: str


@dataclass
class TranslationResult:
    translated_text: str
    source_language: str
    target_language: str
    provider: str
    raw: Optional[Dict[str, Any]] = None


def normalize_text(text: str) -> str:
    return text.strip()


def normalize_texts(texts: List[str]) -> List[str]:
    return [normalize_text(text) for text in texts]
