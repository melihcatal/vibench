from dataclasses import dataclass
from typing import Any, Dict, List, Mapping


@dataclass
class TranslationRequest:
    text: str
    source_language: str = 'auto'
    target_language: str = 'en'


def normalize_text(value: Any) -> str:
    if value is None:
        return ''
    return str(value)


def normalize_text_list(values: List[Any]) -> List[str]:
    return [normalize_text(v) for v in values]


def normalize_mapping_values(values: Mapping[str, Any]) -> Dict[str, str]:
    return {str(k): normalize_text(v) for k, v in values.items()}
