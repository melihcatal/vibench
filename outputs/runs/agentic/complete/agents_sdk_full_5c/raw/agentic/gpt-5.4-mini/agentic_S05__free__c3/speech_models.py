from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Optional


@dataclass(slots=True)
class StreamingChunk:
    audio: bytes
    timestamp_ms: int = 0


@dataclass(slots=True)
class StreamingConfig:
    language: str = "en-US"
    punctuate: bool = True
    connection_id: str = "streaming-connection"


@dataclass(slots=True)
class TranscriptEvent:
    text: str
    is_final: bool
    confidence: float = 0.0
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class CaptionRecord:
    text: str
    is_final: bool
    language: str = "en-US"


def normalize_transcript_event(payload: Any) -> Optional[dict[str, Any]]:
    if payload is None:
        return None
    if isinstance(payload, bytes):
        payload = payload.decode("utf-8", errors="ignore")
    if isinstance(payload, str):
        if payload.strip().startswith("{"):
            data = json.loads(payload)
        else:
            return None
    else:
        data = payload
    if not isinstance(data, dict):
        return None
    text = data.get("DisplayText") or data.get("text") or data.get("transcript", "")
    is_final = bool(data.get("RecognitionStatus") in {"Success", "Final"} or data.get("is_final"))
    return {"text": text, "is_final": is_final, "raw": data}


def normalize_caption_chunks(items: Iterable[CaptionRecord]) -> list[str]:
    return [item.text.strip() for item in items if item.text.strip()]
