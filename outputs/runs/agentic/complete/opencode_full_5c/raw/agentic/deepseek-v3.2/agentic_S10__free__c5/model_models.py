from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class TaskType(Enum):
    SUMMARIZATION = "summarization"
    EXTRACTION = "extraction"
    QA = "qa"
    STREAMING = "streaming"
    TRANSLATION = "translation"
    EMBEDDING = "embedding"
    SAFETY = "safety"


@dataclass
class SummaryRequest:
    text: str
    max_length: int = 200
    model: Optional[str] = None


@dataclass
class SummaryResponse:
    summary: str
    original_length: int
    summary_length: int
    model_used: str


@dataclass
class ExtractRequest:
    text: str
    schema_description: str
    model: Optional[str] = None


@dataclass
class ExtractResponse:
    extracted_data: Dict[str, Any]
    success: bool
    model_used: str


@dataclass
class QARequest:
    question: str
    context: str
    model: Optional[str] = None


@dataclass
class QAResponse:
    answer: str
    confidence: Optional[float] = None
    model_used: str


@dataclass
class StreamRequest:
    prompt: str
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 500


@dataclass
class StreamResponse:
    chunks: List[str]
    full_text: str
    model_used: str


@dataclass
class SafetyRequest:
    text: str
    check_type: str = "both"  # "prompt", "response", or "both"


@dataclass
class SafetyResponse:
    is_safe: bool
    flagged_categories: List[str]
    confidence: float
    provider: str


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass
class TranslationResponse:
    translated_text: str
    source_language: str
    target_language: str
    provider: str


@dataclass
class EmbeddingRequest:
    text: str
    model: Optional[str] = None


@dataclass
class EmbeddingResponse:
    embedding: List[float]
    dimensions: int
    model_used: str


@dataclass
class SpeechRequest:
    text: str
    voice: str = "alloy"
    speed: float = 1.0


@dataclass
class SpeechResponse:
    audio_data: bytes
    format: str
    duration_seconds: float
    provider: str


def normalize_response(response_data: Dict[str, Any], task_type: TaskType) -> Any:
    """Normalize response data from different providers."""
    if task_type == TaskType.SUMMARIZATION:
        return SummaryResponse(
            summary=response_data.get("summary", ""),
            original_length=response_data.get("original_length", 0),
            summary_length=response_data.get("summary_length", 0),
            model_used=response_data.get("model_used", "unknown"),
        )
    elif task_type == TaskType.EXTRACTION:
        return ExtractResponse(
            extracted_data=response_data.get("extracted_data", {}),
            success=response_data.get("success", False),
            model_used=response_data.get("model_used", "unknown"),
        )
    elif task_type == TaskType.QA:
        return QAResponse(
            answer=response_data.get("answer", ""),
            confidence=response_data.get("confidence"),
            model_used=response_data.get("model_used", "unknown"),
        )

    return response_data
