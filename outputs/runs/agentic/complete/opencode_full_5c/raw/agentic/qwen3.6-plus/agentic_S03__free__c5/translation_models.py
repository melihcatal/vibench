from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TranslationRequest:
    text: str
    source_language: str = "en"
    target_language: str = "es"
    model: str = "nmt"
    glossary_config: Optional[dict] = None
    mime_type: str = "text/plain"


@dataclass
class TranslationResult:
    translated_text: str
    source_language: str
    target_language: str
    model: str
    detected_source_language: Optional[str] = None


@dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_language: str = "en"
    target_language: str = "es"
    model: str = "nmt"


@dataclass
class BatchTranslationResult:
    results: List[TranslationResult]
    total_count: int
    successful_count: int


@dataclass
class TranslationQualityIssue:
    segment: str
    issue_type: str
    severity: str
    description: str


@dataclass
class TranslationQualitySummary:
    overall_score: float
    issues: List[TranslationQualityIssue]
    segment_count: int


def normalize_request(request: dict) -> TranslationRequest:
    return TranslationRequest(
        text=request.get("text", ""),
        source_language=request.get("source_language", "en"),
        target_language=request.get("target_language", "es"),
        model=request.get("model", "nmt"),
        glossary_config=request.get("glossary_config"),
        mime_type=request.get("mime_type", "text/plain"),
    )


def normalize_batch_request(request: dict) -> BatchTranslationRequest:
    return BatchTranslationRequest(
        texts=request.get("texts", []),
        source_language=request.get("source_language", "en"),
        target_language=request.get("target_language", "es"),
        model=request.get("model", "nmt"),
    )


def build_response(
    translated_text: str,
    source_lang: str,
    target_lang: str,
    model: str,
    detected_lang: Optional[str] = None,
) -> TranslationResult:
    return TranslationResult(
        translated_text=translated_text,
        source_language=source_lang,
        target_language=target_lang,
        model=model,
        detected_source_language=detected_lang,
    )


def build_batch_response(results: List[TranslationResult]) -> BatchTranslationResult:
    return BatchTranslationResult(
        results=results,
        total_count=len(results),
        successful_count=sum(1 for r in results if r.translated_text),
    )
