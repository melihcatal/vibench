from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Sequence


@dataclass(slots=True)
class TranslationRequest:
    text: str
    source_language: str | None = None
    target_language: str = "en"
    formality: str | None = None
    glossary_id: str | None = None
    context: str | None = None
    model_type: str | None = None
    tag_handling: str | None = None

    def to_deepl_options(self) -> Dict[str, Any]:
        options: Dict[str, Any] = {}
        if self.source_language:
            options["source_lang"] = self.source_language.upper()
        if self.target_language:
            options["target_lang"] = self.target_language.upper()
        if self.formality:
            options["formality"] = self.formality
        if self.glossary_id:
            options["glossary"] = self.glossary_id
        if self.context:
            options["context"] = self.context
        if self.model_type:
            options["model_type"] = self.model_type
        if self.tag_handling:
            options["tag_handling"] = self.tag_handling
        return options


@dataclass(slots=True)
class TranslationResult:
    text: str
    detected_source_language: str | None = None
    billed_characters: int | None = None
    provider: str = "DeepL"
    model: str | None = None
    raw: Any = None

    def as_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "detected_source_language": self.detected_source_language,
            "billed_characters": self.billed_characters,
            "provider": self.provider,
            "model": self.model,
        }


@dataclass(slots=True)
class BatchTranslationResult:
    items: List[TranslationResult] = field(default_factory=list)
    provider: str = "DeepL"

    def texts(self) -> List[str]:
        return [item.text for item in self.items]

    def as_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "items": [item.as_dict() for item in self.items],
        }


@dataclass(slots=True)
class QualitySummary:
    summary: str
    issues: List[str]
    provider: str
    model: str
    raw: Any = None


@dataclass(slots=True)
class SafetyCheckResult:
    is_safe: bool
    categories: Dict[str, float]
    flagged_segments: List[str]
    provider: str
    raw: Any = None


@dataclass(slots=True)
class EmbeddingResult:
    vectors: List[List[float]]
    provider: str
    model: str
    dimensions: int | None = None
    raw: Any = None


@dataclass(slots=True)
class AudioPreviewResult:
    audio: bytes
    content_type: str
    provider: str
    voice: str
    raw: Any = None


def normalize_language_code(language: str | None) -> str | None:
    if language is None:
        return None
    return language.replace("_", "-").upper()



def ensure_text_list(texts: Sequence[str]) -> List[str]:
    normalized = [str(text) for text in texts]
    if not normalized:
        raise ValueError("texts must not be empty")
    return normalized



def normalize_dictionary_values(data: Mapping[str, Any]) -> Dict[str, str]:
    return {str(key): str(value) for key, value in data.items()}
