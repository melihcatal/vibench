from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Sequence, Type, TypeVar


@dataclass(frozen=True)
class TranslationRequest:
    text: str
    source_language: str
    target_language: str


@dataclass(frozen=True)
class BatchTranslationRequest:
    texts: List[str]
    source_language: str
    target_language: str


@dataclass(frozen=True)
class MarkupTranslationRequest:
    markup: str
    source_language: str
    target_language: str


@dataclass(frozen=True)
class DictionaryTranslationRequest:
    data: Dict[str, Any]
    source_language: str
    target_language: str


@dataclass(frozen=True)
class TranslationResult:
    translation: str
    provider: str = "deepl"


@dataclass(frozen=True)
class BatchTranslationResult:
    translations: List[str]
    provider: str = "deepl"


@dataclass(frozen=True)
class MarkupTranslationResult:
    translated_markup: str
    provider: str = "deepl"


@dataclass(frozen=True)
class DictionaryTranslationResult:
    data: Dict[str, Any]
    provider: str = "deepl"


T = TypeVar("T")


def normalize_text(text: str) -> str:
    return " ".join(str(text).split())


def normalize_translation_response(payload: Mapping[str, Any], result_type: Type[T]) -> T:
    if result_type is TranslationResult:
        translations = payload.get("translations", [])
        return result_type(translation=translations[0]["text"] if translations else "")  # type: ignore[return-value]
    if result_type is BatchTranslationResult:
        translations = payload.get("translations", [])
        return result_type(translations=[item["text"] for item in translations])  # type: ignore[return-value]
    if result_type is MarkupTranslationResult:
        translations = payload.get("translations", [])
        return result_type(translated_markup=translations[0]["text"] if translations else "")  # type: ignore[return-value]
    if result_type is DictionaryTranslationResult:
        raise ValueError("Dictionary result requires caller-side assembly")
    raise TypeError("Unsupported result type")
