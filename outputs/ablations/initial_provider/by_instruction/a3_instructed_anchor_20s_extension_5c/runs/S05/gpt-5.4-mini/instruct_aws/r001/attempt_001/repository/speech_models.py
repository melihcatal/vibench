from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional


@dataclass
class StreamingSpeechConfig:
    region: str
    language_code: str = "en-US"
    sample_rate_hz: int = 16000
    media_encoding: str = "pcm"
    enable_partial_results: bool = True
    enable_punctuation: bool = True


@dataclass
class TranscriptResult:
    text: str
    is_partial: bool
    confidence: Optional[float] = None
    language_code: Optional[str] = None


def normalize_transcript_text(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_result_payload(payload: Dict[str, Any]) -> TranscriptResult:
    alternatives = payload.get("Alternatives") or payload.get("alternatives") or []
    item = alternatives[0] if alternatives else {}
    text = item.get("Transcript") or item.get("transcript") or payload.get("Transcript") or ""
    confidence = item.get("Confidence") or item.get("confidence")
    return TranscriptResult(
        text=normalize_transcript_text(text),
        is_partial=bool(payload.get("IsPartial", payload.get("is_partial", False))),
        confidence=float(confidence) if confidence is not None else None,
        language_code=payload.get("LanguageCode") or payload.get("language_code"),
    )


def iter_transcript_text(results: Iterable[TranscriptResult]) -> Iterable[str]:
    for result in results:
        yield result.text
