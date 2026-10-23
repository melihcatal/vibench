from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def _get(d: Dict[str, Any], *keys: str, default: Any = None) -> Any:
    for k in keys:
        if k in d:
            return d[k]
    return default


def normalize_segments(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    if isinstance(payload, dict):
        if isinstance(payload.get("segments"), list):
            return payload["segments"]
        if isinstance(payload.get("results"), list):
            return payload["results"]
        if isinstance(payload.get("items"), list):
            return payload["items"]
    return []


def normalize_transcript_text(payload: Dict[str, Any]) -> str:
    if not isinstance(payload, dict):
        return ""
    if isinstance(payload.get("text"), str):
        return payload["text"]
    if isinstance(payload.get("transcript"), str):
        return payload["transcript"]
    segments = normalize_segments(payload)
    parts = []
    for seg in segments:
        txt = _get(seg, "text", "transcript", default="")
        if txt:
            parts.append(str(txt))
    return " ".join(parts).strip()


@dataclass
class TranscriptionRequest:
    audio_url: str
    language: Optional[str] = None
    diarization: bool = False
    word_timestamps: bool = False

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"audio_url": self.audio_url}
        if self.language:
            payload["language"] = self.language
        if self.diarization:
            payload["diarization"] = True
        if self.word_timestamps:
            payload["word_timestamps"] = True
        return payload


@dataclass
class TranslationRequest:
    text: str
    target_language: str


@dataclass
class ModerationRequest:
    text: str


@dataclass
class SummaryRequest:
    transcript: str


@dataclass
class EmbeddingRequest:
    segments: List[str]
