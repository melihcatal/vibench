from dataclasses import dataclass
from typing import Any, Dict, List, Mapping


@dataclass
class TranslationRequest:
    text: str
    source_language: str = "auto"
    target_language: str = "en"


@dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_language: str = "auto"
    target_language: str = "en"


@dataclass
class TranslationResponse:
    translated_text: str


@dataclass
class BatchTranslationResponse:
    translated_texts: List[str]


@dataclass
class QualitySummaryResponse:
    score: float
    issues: List[str]


@dataclass
class UnsafeCopyCheckResponse:
    unsafe: bool
    findings: List[str]


@dataclass
class EmbeddingResponse:
    vector: List[float]


@dataclass
class AudioPreviewResponse:
    audio_base64: str


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_dictionary_values(data: Mapping[str, Any]) -> Dict[str, str]:
    return {str(key): normalize_text(value) for key, value in data.items()}
