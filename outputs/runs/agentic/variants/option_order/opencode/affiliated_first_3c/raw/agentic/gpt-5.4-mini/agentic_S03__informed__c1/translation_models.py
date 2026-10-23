from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TranslationRequest:
    source_language: str
    target_language: str
    text: Any
    format: str = "text"
    options: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationResponse:
    source_language: str
    target_language: str
    translated: Any
    provider: str
    raw: Optional[Any] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def normalize_text_list(values: Any) -> List[str]:
    if values is None:
        return []
    return [normalize_text(v) for v in values]


def normalize_mapping_values(data: Any) -> Dict[str, str]:
    if data is None:
        return {}
    return {str(k): normalize_text(v) for k, v in dict(data).items()}
