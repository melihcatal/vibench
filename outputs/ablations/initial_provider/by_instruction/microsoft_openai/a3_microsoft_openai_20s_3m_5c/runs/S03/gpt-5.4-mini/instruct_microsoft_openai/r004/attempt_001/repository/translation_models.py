from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TranslationRequest:
    text: str
    source_language: Optional[str] = None
    target_language: str = "en"


@dataclass
class TranslationResult:
    translated_text: str
    source_language: Optional[str] = None
    target_language: str = "en"
    raw: Optional[Dict[str, Any]] = None


def normalize_text(value: Any) -> str:
    return "" if value is None else str(value)


def normalize_text_list(values: Any) -> List[str]:
    if values is None:
        return []
    return [normalize_text(value) for value in values]


def normalize_mapping_values(values: Dict[str, Any]) -> Dict[str, str]:
    return {key: normalize_text(value) for key, value in values.items()}
