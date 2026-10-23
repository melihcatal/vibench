from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TranslationRequest:
    text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    context: Optional[str] = None


@dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_language: Optional[str] = None
    target_language: Optional[str] = None


@dataclass
class TranslationResult:
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchTranslationResult:
    translated_texts: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_text_list(values: Any) -> List[str]:
    if not values:
        return []
    return [normalize_text(v) for v in values]


def normalize_dictionary_values(data: Dict[str, Any]) -> Dict[str, str]:
    return {str(k): normalize_text(v) for k, v in data.items()}
