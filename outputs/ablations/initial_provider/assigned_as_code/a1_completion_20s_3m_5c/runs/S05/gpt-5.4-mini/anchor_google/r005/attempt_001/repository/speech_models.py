from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


def normalize_text(text: Optional[str]) -> str:
    return " ".join((text or "").split())


def normalize_transcript_event(text: str, is_final: bool, confidence: Optional[float] = None) -> Dict[str, Any]:
    payload = {"text": normalize_text(text), "is_final": bool(is_final)}
    if confidence is not None:
        payload["confidence"] = float(confidence)
    return payload


def normalize_chunks(chunks: Iterable[bytes]) -> List[bytes]:
    return [chunk for chunk in chunks if chunk]


@dataclass
class StreamSpeechPayload:
    sample_rate_hz: int
    language_code: str
    audio_chunks: List[bytes]
    enable_automatic_punctuation: bool = False

    @classmethod
    def from_mapping(cls, payload: Dict[str, Any]) -> "StreamSpeechPayload":
        return cls(
            sample_rate_hz=int(payload["sample_rate_hz"]),
            language_code=str(payload["language_code"]),
            audio_chunks=normalize_chunks(payload["audio_chunks"]),
            enable_automatic_punctuation=bool(payload.get("enable_automatic_punctuation", False)),
        )
