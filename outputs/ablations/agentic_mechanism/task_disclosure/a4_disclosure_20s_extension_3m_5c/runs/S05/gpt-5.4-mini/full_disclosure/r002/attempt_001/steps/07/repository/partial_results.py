from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Optional

from google.cloud import speech_v1 as speech


@dataclass(frozen=True)
class StreamingTranscriptEvent:
    text: str
    is_final: bool
    confidence: Optional[float] = None
    stability: Optional[float] = None


def _extract_alt(result: Any) -> Any:
    if hasattr(result, "alternatives") and result.alternatives:
        return result.alternatives[0]
    return None


def _result_text(result: Any) -> str:
    alt = _extract_alt(result)
    if alt is None:
        return ""
    return getattr(alt, "transcript", "") or ""


def _result_confidence(result: Any) -> Optional[float]:
    alt = _extract_alt(result)
    if alt is None:
        return None
    confidence = getattr(alt, "confidence", None)
    if confidence is None:
        return None
    return float(confidence)


def _result_stability(result: Any) -> Optional[float]:
    stability = getattr(result, "stability", None)
    if stability is None:
        return None
    return float(stability)


def iter_streaming_transcript_events(responses: Iterable[Any]) -> Iterable[StreamingTranscriptEvent]:
    for response in responses:
        for result in getattr(response, "results", []) or []:
            text = _result_text(result).strip()
            if not text:
                continue
            yield StreamingTranscriptEvent(
                text=text,
                is_final=bool(getattr(result, "is_final", False)),
                confidence=_result_confidence(result),
                stability=_result_stability(result),
            )


def split_partial_and_final_events(responses: Iterable[Any]) -> tuple[list[str], list[str]]:
    partials: list[str] = []
    finals: list[str] = []
    for event in iter_streaming_transcript_events(responses):
        if event.is_final:
            finals.append(event.text)
        else:
            partials.append(event.text)
    return partials, finals


def is_google_cloud_speech_response(response: Any) -> bool:
    return isinstance(response, speech.StreamingRecognizeResponse) or hasattr(response, "results")
