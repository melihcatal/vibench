from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional


@dataclass
class TranslationRequest:
    source_text: str
    source_language: str
    target_language: str


@dataclass
class TranslationResponse:
    translated_text: str
    detected_source_language: Optional[str] = None
    provider: Optional[str] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_text_list(values: Any) -> List[str]:
    if values is None:
        return []
    return [normalize_text(v) for v in values]


def normalize_mapping_values(values: Mapping[str, Any]) -> Dict[str, str]:
    return {str(k): normalize_text(v) for k, v in values.items()}
