from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional


@dataclass(frozen=True)
class TranslationRequest:
    source_text: Any
    source_language: Optional[str]
    target_language: str
    context: Optional[str] = None


@dataclass(frozen=True)
class TranslationResponse:
    translated_text: Any
    source_language: Optional[str]
    target_language: str
    provider: str


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def normalize_text_list(values: Any) -> List[str]:
    if values is None:
        return []
    return [normalize_text(item) for item in values]


def normalize_dict_values(values: Mapping[str, Any]) -> Dict[str, str]:
    return {str(key): normalize_text(value) for key, value in values.items()}
