from dataclasses import dataclass


@dataclass
class TranscriptEvent:
    text: str
    is_final: bool
    stability: float = 0.0
    language_code: str = "en-US"


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def event_from_result(result, language_code: str = "en-US") -> TranscriptEvent:
    alternative = result.alternatives[0] if result.alternatives else None
    return TranscriptEvent(
        text=normalize_text(alternative.transcript if alternative else ""),
        is_final=bool(getattr(result, "is_final", False)),
        stability=float(getattr(result, "stability", 0.0) or 0.0),
        language_code=language_code,
    )
