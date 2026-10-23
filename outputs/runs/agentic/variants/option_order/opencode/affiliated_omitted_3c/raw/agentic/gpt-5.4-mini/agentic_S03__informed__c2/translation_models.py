from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


@dataclass(frozen=True)
class TranslationRequest:
    source_language: str
    target_language: str
    text: str

    def normalized(self) -> "TranslationRequest":
        return TranslationRequest(
            source_language=_normalize_text(self.source_language),
            target_language=_normalize_text(self.target_language),
            text=_normalize_text(self.text),
        )


@dataclass(frozen=True)
class TranslationResult:
    translated_text: str
    source_language: str
    target_language: str
    provider: str


def normalize_text_list(values: list[Any]) -> list[str]:
    return [_normalize_text(value) for value in values]


def normalize_mapping_values(values: Mapping[str, Any]) -> dict[str, str]:
    return {key: _normalize_text(value) for key, value in values.items()}
