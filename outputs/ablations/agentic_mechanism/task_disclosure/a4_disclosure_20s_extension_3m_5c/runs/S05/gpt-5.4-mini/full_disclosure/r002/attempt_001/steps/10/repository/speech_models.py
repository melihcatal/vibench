from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Optional

from google.cloud import speech_v1p1beta1 as speech


@dataclass(frozen=True)
class StreamingRequestChunk:
    audio_content: bytes


@dataclass(frozen=True)
class StreamingTranscript:
    text: str
    is_final: bool
    confidence: Optional[float] = None
    stability: Optional[float] = None


def normalize_transcript_text(text: str) -> str:
    return " ".join(text.split()).strip()


def normalize_confidence(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def normalize_streaming_request(audio_content: bytes) -> speech.StreamingRecognizeRequest:
    return speech.StreamingRecognizeRequest(audio_content=audio_content)


def normalize_streaming_request_chunks(chunks: Iterable[bytes]) -> list[speech.StreamingRecognizeRequest]:
    return [normalize_streaming_request(chunk) for chunk in chunks if chunk]


def _first_alternative(result: Any) -> Any:
    alternatives = getattr(result, "alternatives", None) or []
    return alternatives[0] if alternatives else None


def normalize_streaming_response_result(result: Any) -> Optional[StreamingTranscript]:
    alternative = _first_alternative(result)
    if alternative is None:
        return None
    text = normalize_transcript_text(getattr(alternative, "transcript", "") or "")
    if not text:
        return None
    return StreamingTranscript(
        text=text,
        is_final=bool(getattr(result, "is_final", False)),
        confidence=normalize_confidence(getattr(alternative, "confidence", None)),
        stability=normalize_confidence(getattr(result, "stability", None)),
    )


def normalize_streaming_response(response: Any) -> list[StreamingTranscript]:
    results = getattr(response, "results", None) or []
    normalized: list[StreamingTranscript] = []
    for result in results:
        transcript = normalize_streaming_response_result(result)
        if transcript is not None:
            normalized.append(transcript)
    return normalized


def extract_final_transcripts(response: Any) -> list[str]:
    return [item.text for item in normalize_streaming_response(response) if item.is_final]


def extract_partial_transcripts(response: Any) -> list[str]:
    return [item.text for item in normalize_streaming_response(response) if not item.is_final]
