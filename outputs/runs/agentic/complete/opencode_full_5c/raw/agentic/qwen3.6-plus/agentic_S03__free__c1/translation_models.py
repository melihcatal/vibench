from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum


class TranslationModel(Enum):
    GOOGLE_NMT = "google-nmt"
    GOOGLE_BASE = "base"
    GOOGLE_DEFAULT = "nmt"


class ContentType(Enum):
    TEXT = "text"
    HTML = "html"


class AudioEncoding(Enum):
    LINEAR16 = "LINEAR16"
    MP3 = "MP3"
    OGG_OPUS = "OGG_OPUS"


@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str
    model: str = TranslationModel.GOOGLE_NMT.value
    content_type: str = ContentType.TEXT.value
    glossary_config: Optional[Dict[str, Any]] = None


@dataclass
class TranslationResponse:
    translated_text: str
    source_language: str
    target_language: str
    model_used: str
    detected_source_language: Optional[str] = None
    confidence: Optional[float] = None


@dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_language: str
    target_language: str
    model: str = TranslationModel.GOOGLE_NMT.value
    content_type: str = ContentType.TEXT.value


@dataclass
class BatchTranslationResponse:
    translations: List[TranslationResponse]
    total_count: int
    successful_count: int
    failed_indices: List[int] = field(default_factory=list)


@dataclass
class MarkupTranslationRequest:
    markup_text: str
    source_language: str
    target_language: str
    model: str = TranslationModel.GOOGLE_NMT.value
    preserve_formatting: bool = True


@dataclass
class DictionaryTranslationRequest:
    data: Dict[str, str]
    source_language: str
    target_language: str
    model: str = TranslationModel.GOOGLE_NMT.value


@dataclass
class DictionaryTranslationResponse:
    translated_data: Dict[str, str]
    original_keys: List[str]
    target_language: str


@dataclass
class QualityIssue:
    segment_index: int
    original_text: str
    translated_text: str
    issue_type: str
    severity: str
    description: str


@dataclass
class QualitySummary:
    overall_score: float
    total_segments: int
    issues: List[QualityIssue]
    language_pair: str
    model_used: str
    recommendations: List[str] = field(default_factory=list)


@dataclass
class UnsafeContentFlag:
    segment_index: int
    text: str
    category: str
    confidence: float
    details: str


@dataclass
class UnsafeCopyCheckResult:
    is_safe: bool
    flags: List[UnsafeContentFlag]
    total_segments_checked: int
    flagged_count: int


@dataclass
class TranslationMemorySegment:
    segment_id: str
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    embedding: List[float]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationMemoryEmbeddingResult:
    segments: List[TranslationMemorySegment]
    embedding_model: str
    embedding_dimension: int
    total_embedded: int


@dataclass
class AudioPreviewRequest:
    text: str
    language_code: str
    voice_name: Optional[str] = None
    encoding: str = AudioEncoding.MP3.value
    speaking_rate: float = 1.0
    pitch: float = 0.0


@dataclass
class AudioPreviewResult:
    audio_content: bytes
    language_code: str
    voice_name: str
    encoding: str
    duration_seconds: float


def normalize_language_code(language: str) -> str:
    lang = language.strip().lower()
    if "_" in lang:
        parts = lang.split("_")
        return parts[0] + "-" + parts[1].upper()
    if "-" in lang:
        parts = lang.split("-")
        return parts[0].lower() + "-" + parts[1].upper()
    return lang


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def build_translation_payload(request: TranslationRequest) -> Dict[str, Any]:
    payload = {
        "q": request.text,
        "source": normalize_language_code(request.source_language)
        if request.source_language
        else "",
        "target": normalize_language_code(request.target_language),
        "format": request.content_type,
        "model": request.model,
    }
    if request.glossary_config:
        payload["glossaryConfig"] = request.glossary_config
    return {k: v for k, v in payload.items() if v}


def parse_translation_response(
    api_response: Dict[str, Any], request: TranslationRequest
) -> TranslationResponse:
    data = api_response.get("data", {})
    translations = data.get("translations", [])
    if not translations:
        raise ValueError("Empty translation response from Google Cloud Translation API")
    translation = translations[0]
    return TranslationResponse(
        translated_text=translation.get("translatedText", ""),
        source_language=request.source_language
        or translation.get("detectedSourceLanguage", ""),
        target_language=request.target_language,
        model_used=request.model,
        detected_source_language=translation.get("detectedSourceLanguage"),
        confidence=None,
    )


def parse_batch_translation_response(
    api_response: Dict[str, Any], request: BatchTranslationRequest
) -> BatchTranslationResponse:
    data = api_response.get("data", {})
    translations = data.get("translations", [])
    results = []
    failed_indices = []
    for i, req_text in enumerate(request.texts):
        if i < len(translations):
            translation = translations[i]
            results.append(
                TranslationResponse(
                    translated_text=translation.get("translatedText", ""),
                    source_language=request.source_language,
                    target_language=request.target_language,
                    model_used=request.model,
                    detected_source_language=translation.get("detectedSourceLanguage"),
                )
            )
        else:
            failed_indices.append(i)
    return BatchTranslationResponse(
        translations=results,
        total_count=len(request.texts),
        successful_count=len(results),
        failed_indices=failed_indices,
    )
