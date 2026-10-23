from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class StreamingTranscriptEvent:
    text: str
    is_final: bool
    stability: Optional[float] = None
    provider: str = "google-cloud-speech"
    raw: Optional[Dict[str, Any]] = None


def _get_attr(obj: Any, name: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def parse_streaming_result(result: Any) -> Optional[StreamingTranscriptEvent]:
    alternatives = _get_attr(result, "alternatives", []) or []
    if not alternatives:
        return None
    top = alternatives[0]
    transcript = _get_attr(top, "transcript", "") or ""
    is_final = bool(_get_attr(result, "is_final", _get_attr(result, "isFinal", False)))
    stability = _get_attr(result, "stability", None)
    return StreamingTranscriptEvent(text=transcript, is_final=is_final, stability=stability, raw=result if isinstance(result, dict) else None)


def handle_partial_and_final_results(result: Any) -> Dict[str, Any]:
    event = parse_streaming_result(result)
    if event is None:
        return {"text": "", "is_final": False, "event_type": "empty", "provider": "google-cloud-speech"}
    return {
        "text": event.text,
        "is_final": event.is_final,
        "event_type": "final" if event.is_final else "partial",
        "stability": event.stability,
        "provider": event.provider,
        "raw": event.raw,
    }
