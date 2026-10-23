from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class TranslationRequest:
    text: str
    source_lang: str
    target_lang: str


@dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_lang: str
    target_lang: str


def normalize_text(value: Any) -> str:
    return "" if value is None else str(value)


def normalize_mapping_values(data: Dict[str, Any]) -> Dict[str, str]:
    return {key: normalize_text(value) for key, value in data.items()}
