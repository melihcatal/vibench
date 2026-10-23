from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass
class TranslationRequest:
    source_text: Any
    source_language: str
    target_language: str
    preserve_formatting: bool = False


@dataclass
class TranslationResponse:
    translated_text: Any
    source_language: str
    target_language: str
    provider: str


def normalize_text(text: Any) -> str:
    if text is None:
        return ""
    return str(text)


def normalize_text_list(values: Iterable[Any]) -> List[str]:
    return [normalize_text(v) for v in values]


def normalize_mapping_values(values: Mapping[str, Any]) -> Dict[str, str]:
    return {k: normalize_text(v) for k, v in values.items()}
