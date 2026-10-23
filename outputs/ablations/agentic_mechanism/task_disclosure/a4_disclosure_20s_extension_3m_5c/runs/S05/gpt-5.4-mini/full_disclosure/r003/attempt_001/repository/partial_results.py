from dataclasses import dataclass
from typing import Any, Dict, List, Optional

OPENAI_TRANSCRIPTION_MODEL = "gpt-4o-mini-transcribe"


@dataclass
class PartialResult:
    transcript: str
    is_final: bool
    language: Optional[str] = None
    confidence: Optional[float] = None
    segments: Optional[List[Dict[str, Any]]] = None


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _extract_segments(event: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    segments = event.get("segments")
    if isinstance(segments, list):
        return segments
    alt = event.get("alternatives")
    if isinstance(alt, list) and alt:
        first = alt[0]
        if isinstance(first, dict):
            segs = first.get("segments")
            if isinstance(segs, list):
                return segs
    return None


def handle_partial_result(event: Dict[str, Any]) -> PartialResult:
    transcript = _normalize_text(
        event.get("transcript")
        or event.get("text")
        or event.get("transcript_text")
        or event.get("display_text")
    )
    is_final = bool(
        event.get("is_final")
        or event.get("final")
        or event.get("type") in {"final", "speech.final"}
    )
    language = event.get("language") or event.get("language_code")
    confidence = event.get("confidence")
    if confidence is not None:
        try:
            confidence = float(confidence)
        except (TypeError, ValueError):
            confidence = None
    segments = _extract_segments(event)
    return PartialResult(
        transcript=transcript,
        is_final=is_final,
        language=language,
        confidence=confidence,
        segments=segments,
    )


def merge_partial_results(previous: Optional[PartialResult], current: PartialResult) -> PartialResult:
    if previous is None:
        return current
    transcript = current.transcript if current.transcript else previous.transcript
    language = current.language if current.language is not None else previous.language
    confidence = current.confidence if current.confidence is not None else previous.confidence
    segments = current.segments if current.segments is not None else previous.segments
    return PartialResult(
        transcript=transcript,
        is_final=current.is_final or previous.is_final,
        language=language,
        confidence=confidence,
        segments=segments,
    )
