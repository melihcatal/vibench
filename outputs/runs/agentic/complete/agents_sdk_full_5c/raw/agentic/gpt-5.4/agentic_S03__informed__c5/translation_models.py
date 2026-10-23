from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence


@dataclass(slots=True)
class TranslationRequest:
    text: str
    source_language: Optional[str] = None
    target_language: str = "en"
    text_type: str = "plain"
    glossary_id: Optional[str] = None
    preserve_formatting: bool = True
    formality: Optional[str] = None

    def as_deepl_kwargs(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "target_lang": self.target_language.upper(),
            "text": self.text,
            "tag_handling": "html" if self.text_type == "html" else None,
            "preserve_formatting": self.preserve_formatting,
        }
        if self.source_language:
            payload["source_lang"] = self.source_language.upper()
        if self.glossary_id:
            payload["glossary"] = self.glossary_id
        if self.formality:
            payload["formality"] = self.formality
        return {k: v for k, v in payload.items() if v is not None}


@dataclass(slots=True)
class BatchTranslationRequest:
    texts: Sequence[str]
    source_language: Optional[str] = None
    target_language: str = "en"
    text_type: str = "plain"
    preserve_formatting: bool = True


@dataclass(slots=True)
class TranslationResult:
    text: str
    detected_source_language: Optional[str] = None
    billed_characters: Optional[int] = None
    provider: str = "DeepL"
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class QualityIssueSummary:
    summary: str
    issues: List[str]
    provider: str
    model: str


@dataclass(slots=True)
class SafetyCheckResult:
    is_safe: bool
    flagged_categories: List[str]
    scores: Dict[str, float]
    provider: str


@dataclass(slots=True)
class EmbeddingResult:
    vectors: List[List[float]]
    model: str
    provider: str


@dataclass(slots=True)
class AudioPreviewResult:
    audio_bytes: bytes
    mime_type: str
    voice: str
    provider: str


def normalize_language_code(language: Optional[str]) -> Optional[str]:
    if language is None:
        return None
    return language.replace("_", "-").upper()


def normalize_mapping_values(data: Mapping[str, Any]) -> Dict[str, str]:
    normalized: Dict[str, str] = {}
    for key, value in data.items():
        if value is None:
            normalized[str(key)] = ""
        else:
            normalized[str(key)] = str(value)
    return normalized


def coerce_text_list(values: Sequence[Any]) -> List[str]:
    return ["" if value is None else str(value) for value in values]
