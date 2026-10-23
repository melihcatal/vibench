from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class StreamingRecognitionRequest:
    audio_content: bytes


@dataclass
class StreamingRecognitionResponse:
    transcript: str
    is_final: bool
    language: Optional[str] = None
    confidence: Optional[float] = None
    segments: Optional[List[Dict[str, Any]]] = None
    raw: Optional[Dict[str, Any]] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on", "final"}
    return bool(value)


def normalize_confidence(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def extract_segments(event: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    segments = event.get("segments")
    if isinstance(segments, list):
        return segments
    alternatives = event.get("alternatives")
    if isinstance(alternatives, list) and alternatives:
        first = alternatives[0]
        if isinstance(first, dict):
            alt_segments = first.get("segments")
            if isinstance(alt_segments, list):
                return alt_segments
    return None


def normalize_streaming_response(event: Dict[str, Any]) -> StreamingRecognitionResponse:
    transcript = normalize_text(
        event.get("transcript")
        or event.get("text")
        or event.get("transcript_text")
        or event.get("display_text")
    )
    is_final = normalize_bool(event.get("is_final") or event.get("final") or event.get("type") in {"final", "speech.final"})
    language = event.get("language") or event.get("language_code")
    confidence = normalize_confidence(event.get("confidence"))
    return StreamingRecognitionResponse(
        transcript=transcript,
        is_final=is_final,
        language=language,
        confidence=confidence,
        segments=extract_segments(event),
        raw=event,
    )


def merge_streaming_responses(previous: Optional[StreamingRecognitionResponse], current: StreamingRecognitionResponse) -> StreamingRecognitionResponse:
    if previous is None:
        return current
    return StreamingRecognitionResponse(
        transcript=current.transcript if current.transcript else previous.transcript,
        is_final=current.is_final or previous.is_final,
        language=current.language if current.language is not None else previous.language,
        confidence=current.confidence if current.confidence is not None else previous.confidence,
        segments=current.segments if current.segments is not None else previous.segments,
        raw=current.raw if current.raw is not None else previous.raw,
    )
