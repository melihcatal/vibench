from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str


@dataclass
class TranslationResult:
    translated_text: str
    source_language: str
    target_language: str


@dataclass
class BatchTranslationResult:
    translated_texts: List[str]


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_mapping_values(data: Dict[str, Any]) -> Dict[str, str]:
    return {str(key): normalize_text(value) for key, value in data.items()}
