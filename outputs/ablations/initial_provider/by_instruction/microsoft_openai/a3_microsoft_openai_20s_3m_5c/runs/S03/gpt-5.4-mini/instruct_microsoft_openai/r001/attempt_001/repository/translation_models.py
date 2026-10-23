from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TranslationRequest:
    text: str
    source_language: Optional[str] = None
    target_language: str = "en"
    preserve_tags: bool = False


@dataclass
class TranslationResult:
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def normalize_text_list(values: List[Any]) -> List[str]:
    return [normalize_text(v) for v in values]


def normalize_dict_values(values: Dict[str, Any]) -> Dict[str, str]:
    return {str(k): normalize_text(v) for k, v in values.items()}
