from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class TranslationRequest:
    source_text: str
    source_lang: str
    target_lang: str


@dataclass
class TranslationResponse:
    translated_text: str
    source_lang: str
    target_lang: str
    confidence: float = 1.0


@dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_lang: str
    target_lang: str


@dataclass
class BatchTranslationResponse:
    translations: List[TranslationResponse]
    source_lang: str
    target_lang: str


@dataclass
class MarkupTranslationRequest:
    html_content: str
    source_lang: str
    target_lang: str


@dataclass
class MarkupTranslationResponse:
    translated_markup: str
    source_lang: str
    target_lang: str


@dataclass
class DictionaryTranslationRequest:
    dictionary: Dict[str, Any]
    source_lang: str
    target_lang: str


@dataclass
class DictionaryTranslationResponse:
    translated_dictionary: Dict[str, str]
    source_lang: str
    target_lang: str


@dataclass
class QualitySummaryRequest:
    translations: List[TranslationResponse]
    source_lang: str
    target_lang: str
    context: Optional[str] = None


@dataclass
class QualitySummaryResponse:
    overall_score: float
    issues: List[Dict[str, Any]]
    summary: str


@dataclass
class UnsafeCopyCheckRequest:
    text: str
    target_lang: str
    categories: Optional[List[str]] = None


@dataclass
class UnsafeCopyCheckResponse:
    is_safe: bool
    flagged_categories: List[str]
    details: List[Dict[str, Any]]


@dataclass
class TranslationMemoryEmbedRequest:
    segments: List[str]
    source_lang: str
    target_lang: str


@dataclass
class TranslationMemoryEmbedResponse:
    embeddings: List[List[float]]
    segment_count: int
    model: str


@dataclass
class LocalizedAudioPreviewRequest:
    text: str
    target_lang: str
    voice_id: Optional[str] = None


@dataclass
class LocalizedAudioPreviewResponse:
    audio_url: str
    duration_seconds: float
    voice_id: str


def normalize_translation_response(data: Dict[str, Any]) -> TranslationResponse:
    return TranslationResponse(
        translated_text=data.get("translated_text", ""),
        source_lang=data.get("source_lang", ""),
        target_lang=data.get("target_lang", ""),
        confidence=data.get("confidence", 1.0),
    )


def normalize_batch_response(data: Dict[str, Any]) -> BatchTranslationResponse:
    translations = [
        normalize_translation_response(t) for t in data.get("translations", [])
    ]
    return BatchTranslationResponse(
        translations=translations,
        source_lang=data.get("source_lang", ""),
        target_lang=data.get("target_lang", ""),
    )
