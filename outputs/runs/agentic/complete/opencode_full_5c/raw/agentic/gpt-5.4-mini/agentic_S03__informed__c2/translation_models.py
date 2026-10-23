from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Sequence


@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str


@dataclass
class BatchTranslationRequest:
    texts: Sequence[str]
    source_language: str
    target_language: str


def normalize_text(text: str) -> str:
    return ' '.join(text.split())


def normalize_texts(texts: Sequence[str]) -> List[str]:
    return [normalize_text(text) for text in texts]


def normalize_dict_values(data: Mapping[str, Any]) -> Dict[str, str]:
    return {key: normalize_text(str(value)) for key, value in data.items()}
