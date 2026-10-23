from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class TranslationRequest:
    text: str
    source_lang: str | None
    target_lang: str


@dataclass(frozen=True)
class BatchTranslationRequest:
    texts: List[str]
    source_lang: str | None
    target_lang: str


@dataclass(frozen=True)
class TranslationResult:
    translated_text: str
    source_lang: str | None
    target_lang: str


def normalize_translated_text(value: Any) -> str:
    if hasattr(value, "text"):
        return str(value.text)
    return str(value)


def normalize_dictionary_values(
    items: Dict[str, str], translations: Dict[str, str]
) -> Dict[str, str]:
    return {key: translations.get(key, value) for key, value in items.items()}
