from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TranslationRequest:
    text: str
    source_language: Optional[str]
    target_language: str


@dataclass
class TranslationResult:
    translated_text: str
    source_language: Optional[str]
    target_language: str
    provider: str


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def normalize_text_list(values: List[Any]) -> List[str]:
    return [normalize_text(value) for value in values]


def normalize_mapping_values(values: Dict[str, Any]) -> Dict[str, str]:
    return {key: normalize_text(value) for key, value in values.items()}
