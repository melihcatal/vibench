from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptionRequest:
    audio_url: str
    language_code: Optional[str] = None
    diarization: bool = False
    timestamps: str = "segment"
    format: str = "json"


@dataclass
class TranscriptionResult:
    id: str
    status: str
    text: str
    segments: List[Dict[str, Any]]
    metadata: Dict[str, Any]


def normalize_segments(items: Any) -> List[Dict[str, Any]]:
    if not items:
        return []
    normalized = []
    for item in items:
        normalized.append(
            {
                "start": item.get("start"),
                "end": item.get("end"),
                "text": item.get("text", ""),
                "speaker": item.get("speaker"),
                "words": item.get("words", []),
            }
        )
    return normalized


def normalize_transcript(payload: Dict[str, Any]) -> TranscriptionResult:
    return TranscriptionResult(
        id=str(payload.get("id", "")),
        status=str(payload.get("status", "")),
        text=str(payload.get("text", payload.get("transcript", ""))),
        segments=normalize_segments(
            payload.get("segments") or payload.get("utterances") or []
        ),
        metadata={
            k: v
            for k, v in payload.items()
            if k not in {"id", "status", "text", "transcript", "segments", "utterances"}
        },
    )
