from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptionRequest:
    file_path: str
    model: str = "gpt-4o-transcribe"
    language: Optional[str] = None
    prompt: Optional[str] = None
    response_format: str = "json"
    timestamp_granularities: Optional[List[str]] = None
    include: Optional[List[str]] = None
    temperature: Optional[float] = None
    diarize: bool = False


@dataclass
class TranscriptionResult:
    text: str
    raw: Dict[str, Any]
    job_id: Optional[str] = None


@dataclass
class ModerationResult:
    flagged: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]
    raw: Dict[str, Any]


@dataclass
class TranslationResult:
    text: str
    raw: Dict[str, Any]


@dataclass
class EmbeddingResult:
    vector: List[float]
    raw: Dict[str, Any]


def normalize_transcription_response(response: Any) -> TranscriptionResult:
    text = getattr(response, "text", None) or getattr(response, "transcript", None) or ""
    raw = response.model_dump() if hasattr(response, "model_dump") else dict(response)
    job_id = raw.get("id") or raw.get("job_id")
    return TranscriptionResult(text=text, raw=raw, job_id=job_id)
