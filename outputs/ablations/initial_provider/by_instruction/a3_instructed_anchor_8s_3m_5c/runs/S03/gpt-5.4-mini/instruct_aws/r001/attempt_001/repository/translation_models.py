from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TranslationRequest:
    text: str
    source_language_code: str
    target_language_code: str
    settings: Optional[Dict[str, Any]] = None


@dataclass
class TranslationResponse:
    translated_text: str
    source_language_code: str
    target_language_code: str
    provider: str
    raw: Optional[Dict[str, Any]] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_text_list(values: List[Any]) -> List[str]:
    return [normalize_text(value) for value in values]


def normalize_dict_values(values: Dict[str, Any]) -> Dict[str, str]:
    return {key: normalize_text(value) for key, value in values.items()}
