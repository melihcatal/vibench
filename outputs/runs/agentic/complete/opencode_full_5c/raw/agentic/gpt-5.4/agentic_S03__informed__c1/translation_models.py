from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class TranslationRequest:
    text: str
    source_language: str
    target_language: str
    formality: str | None = None
    preserve_formatting: bool = True
    tag_handling: str | None = None
    glossary_id: str | None = None

    def to_deepl_kwargs(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "source_lang": normalize_language_code(self.source_language),
            "target_lang": normalize_language_code(self.target_language),
            "preserve_formatting": self.preserve_formatting,
        }
        if self.formality:
            payload["formality"] = self.formality
        if self.tag_handling:
            payload["tag_handling"] = self.tag_handling
        if self.glossary_id:
            payload["glossary"] = self.glossary_id
        return payload


@dataclass(slots=True)
class TranslationItem:
    text: str
    detected_source_language: str | None = None
    billed_characters: int | None = None
    provider: str = "DeepL"
    model: str = "DeepL API"


@dataclass(slots=True)
class BatchTranslationResponse:
    items: list[TranslationItem] = field(default_factory=list)
    provider: str = "DeepL"
    model: str = "DeepL API"


def normalize_language_code(value: str) -> str:
    return value.strip().replace("-", "_").upper()


def translation_item_from_deepl(
    result: Any, billed_characters: int | None = None
) -> TranslationItem:
    return TranslationItem(
        text=getattr(result, "text", ""),
        detected_source_language=getattr(result, "detected_source_lang", None),
        billed_characters=billed_characters,
    )
