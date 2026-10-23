from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence


@dataclass
class TranslationRequest:
    text: str
    source_language: Optional[str]
    target_language: str
    content_type: str = "plain"


@dataclass
class BatchTranslationRequest:
    texts: Sequence[str]
    source_language: Optional[str]
    target_language: str
    content_type: str = "plain"


@dataclass
class TranslationResult:
    text: str
    detected_source_language: Optional[str] = None
    provider: str = "DeepL"
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchTranslationResult:
    translations: List[TranslationResult]
    provider: str = "DeepL"
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_language_code(language: Optional[str]) -> Optional[str]:
    if language is None:
        return None
    normalized = language.strip().replace("_", "-")
    return normalized.upper() or None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def build_text_items(texts: Sequence[Any]) -> List[str]:
    return [normalize_text(text) for text in texts]


def normalize_mapping_values(data: Mapping[str, Any]) -> Dict[str, str]:
    return {str(key): normalize_text(value) for key, value in data.items()}
