from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str
    tone: Optional[str] = None


@dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_language: str
    target_language: str


@dataclass
class TranslationResponse:
    translated_text: str
    source_language: str
    target_language: str
    provider: str


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_text_list(values: Any) -> List[str]:
    if not values:
        return []
    return [normalize_text(v) for v in values]


def normalize_dict_values(payload: Dict[str, Any]) -> Dict[str, str]:
    return {str(k): normalize_text(v) for k, v in payload.items()}
