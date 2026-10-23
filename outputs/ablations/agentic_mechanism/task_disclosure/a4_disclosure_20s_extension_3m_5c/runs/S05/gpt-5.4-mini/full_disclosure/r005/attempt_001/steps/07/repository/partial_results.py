from dataclasses import dataclass
from typing import Any, Callable, Iterable, List, Optional


@dataclass(frozen=True)
class PartialResultEvent:
    text: str
    is_final: bool
    confidence: Optional[float] = None
    provider: str = "openai"


def _coerce_text(payload: Any) -> str:
    if payload is None:
        return ""
    if isinstance(payload, str):
        return payload
    for key in ("text", "transcript", "caption", "utterance"):
        value = getattr(payload, key, None) if not isinstance(payload, dict) else payload.get(key)
        if isinstance(value, str) and value:
            return value
    return str(payload)


def _coerce_is_final(payload: Any) -> bool:
    if isinstance(payload, bool):
        return payload
    if isinstance(payload, dict):
        for key in ("is_final", "final", "done", "stable"):
            if key in payload:
                return bool(payload[key])
    for key in ("is_final", "final", "done", "stable"):
        value = getattr(payload, key, None)
        if value is not None:
            return bool(value)
    return False


def _coerce_confidence(payload: Any) -> Optional[float]:
    if isinstance(payload, dict):
        for key in ("confidence", "score", "probability"):
            if key in payload and payload[key] is not None:
                try:
                    return float(payload[key])
                except (TypeError, ValueError):
                    return None
    for key in ("confidence", "score", "probability"):
        value = getattr(payload, key, None)
        if value is not None:
            try:
                return float(value)
            except (TypeError, ValueError):
                return None
    return None


def normalize_partial_result(payload: Any) -> PartialResultEvent:
    return PartialResultEvent(
        text=_coerce_text(payload).strip(),
        is_final=_coerce_is_final(payload),
        confidence=_coerce_confidence(payload),
    )


def merge_partial_results(events: Iterable[Any]) -> List[PartialResultEvent]:
    merged: List[PartialResultEvent] = []
    last_partial_text = ""
    for event in events:
        normalized = normalize_partial_result(event)
        if not normalized.text:
            continue
        if normalized.is_final:
            merged.append(normalized)
            last_partial_text = ""
            continue
        if normalized.text != last_partial_text:
            merged.append(normalized)
            last_partial_text = normalized.text
    return merged


def build_stream_event_handler(on_partial: Callable[[PartialResultEvent], None], on_final: Callable[[PartialResultEvent], None]) -> Callable[[Any], None]:
    def handler(payload: Any) -> None:
        event = normalize_partial_result(payload)
        if not event.text:
            return
        if event.is_final:
            on_final(event)
        else:
            on_partial(event)

    return handler
