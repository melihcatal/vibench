from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional


@dataclass
class TranslationRequest:
    text: str
    source_language: Optional[str]
    target_language: str
    preserve_formatting: bool = True


@dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_language: Optional[str]
    target_language: str
    preserve_formatting: bool = True


@dataclass
class TranslationResult:
    provider: str
    translated_text: str
    detected_source_language: Optional[str]
    target_language: str


@dataclass
class BatchTranslationResult:
    provider: str
    translations: List[str]
    detected_source_language: Optional[str]
    target_language: str


def normalize_language_code(language: Optional[str]) -> Optional[str]:
    if language is None:
        return None
    normalized = language.strip().lower().replace("_", "-")
    return normalized or None


def normalize_text(text: Any) -> str:
    if text is None:
        return ""
    return str(text)


def normalize_text_list(texts: List[Any]) -> List[str]:
    return [normalize_text(item) for item in texts]


def normalize_mapping_values(data: Mapping[str, Any]) -> Dict[str, str]:
    return {str(key): normalize_text(value) for key, value in data.items()}
