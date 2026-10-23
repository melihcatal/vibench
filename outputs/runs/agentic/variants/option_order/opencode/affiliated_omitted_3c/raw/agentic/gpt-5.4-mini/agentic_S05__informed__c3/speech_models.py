from dataclasses import dataclass


@dataclass
class TranscriptEvent:
    text: str
    is_final: bool = False
    confidence: float | None = None


def event_from_dict(payload: dict) -> TranscriptEvent:
    return TranscriptEvent(
        text=str(payload.get("text", "")).strip(),
        is_final=bool(payload.get("is_final", False)),
        confidence=payload.get("confidence"),
    )
