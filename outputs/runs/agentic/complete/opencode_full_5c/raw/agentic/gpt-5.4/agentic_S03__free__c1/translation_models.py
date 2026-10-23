from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional


@dataclass
class TranslationRequest:
    text: str
    source_language: Optional[str]
    target_language: str
    text_type: str = "plain"

    def to_deepl_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "text": [self.text],
            "target_lang": self.target_language.upper(),
            "tag_handling": "html" if self.text_type == "html" else None,
        }
        if self.source_language:
            payload["source_lang"] = self.source_language.upper()
        return {k: v for k, v in payload.items() if v is not None}


@dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_language: Optional[str]
    target_language: str
    text_type: str = "plain"

    def to_deepl_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "text": self.texts,
            "target_lang": self.target_language.upper(),
            "tag_handling": "html" if self.text_type == "html" else None,
        }
        if self.source_language:
            payload["source_lang"] = self.source_language.upper()
        return {k: v for k, v in payload.items() if v is not None}


@dataclass
class TranslationResult:
    provider: str
    translated_text: str
    detected_source_language: Optional[str] = None
    billed_characters: Optional[int] = None
    raw: Optional[Mapping[str, Any]] = None


@dataclass
class BatchTranslationResult:
    provider: str
    translations: List[str]
    detected_source_languages: List[Optional[str]]
    raw: Optional[Mapping[str, Any]] = None


def normalize_deepl_translation_response(
    data: Mapping[str, Any],
) -> BatchTranslationResult:
    items = list(data.get("translations", []))
    return BatchTranslationResult(
        provider="DeepL",
        translations=[str(item.get("text", "")) for item in items],
        detected_source_languages=[
            item.get("detected_source_language") for item in items
        ],
        raw=data,
    )


def extract_dictionary_values(data: Mapping[str, Any]) -> List[str]:
    return [str(value) for value in data.values()]


def merge_dictionary_values(
    original: Mapping[str, Any], translated_values: List[str]
) -> Dict[str, str]:
    keys = list(original.keys())
    return {key: translated_values[index] for index, key in enumerate(keys)}
