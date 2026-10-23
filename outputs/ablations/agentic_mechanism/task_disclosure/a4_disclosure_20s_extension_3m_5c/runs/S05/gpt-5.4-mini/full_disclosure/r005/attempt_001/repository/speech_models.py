from dataclasses import dataclass
from typing import Any, Optional


@dataclass(frozen=True)
class SpeechRequest:
    audio: Any
    model: str = "gpt-4o-mini-transcribe"
    language: str = "en"
    temperature: float = 0.0


@dataclass(frozen=True)
class SpeechResponse:
    text: str
    is_final: bool = True
    confidence: Optional[float] = None
    language: Optional[str] = None
    provider: str = "openai"


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    for key in ("text", "transcript", "caption", "utterance"):
        if isinstance(value, dict) and key in value and isinstance(value[key], str):
            return value[key].strip()
        attr = getattr(value, key, None)
        if isinstance(attr, str):
            return attr.strip()
    return str(value).strip()


def normalize_is_final(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, dict):
        for key in ("is_final", "final", "done", "stable"):
            if key in value:
                return bool(value[key])
    for key in ("is_final", "final", "done", "stable"):
        attr = getattr(value, key, None)
        if attr is not None:
            return bool(attr)
    return False


def normalize_confidence(value: Any) -> Optional[float]:
    if isinstance(value, dict):
        for key in ("confidence", "score", "probability"):
            if key in value and value[key] is not None:
                try:
                    return float(value[key])
                except (TypeError, ValueError):
                    return None
    for key in ("confidence", "score", "probability"):
        attr = getattr(value, key, None)
        if attr is not None:
            try:
                return float(attr)
            except (TypeError, ValueError):
                return None
    return None


def normalize_language(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        return value.strip() or None
    for key in ("language", "language_code", "lang"):
        if isinstance(value, dict) and key in value and isinstance(value[key], str):
            return value[key].strip() or None
        attr = getattr(value, key, None)
        if isinstance(attr, str):
            return attr.strip() or None
    return None


def normalize_speech_response(payload: Any) -> SpeechResponse:
    return SpeechResponse(
        text=normalize_text(payload),
        is_final=normalize_is_final(payload),
        confidence=normalize_confidence(payload),
        language=normalize_language(payload),
    )
