from dataclasses import dataclass
from typing import Any


@dataclass
class TranscriptionRequest:
    audio_path: str
    language: str | None = None


@dataclass
class TranscriptionResponse:
    job_id: str
    status: str
    text: str | None = None
    raw: Any | None = None


def normalize_transcript_text(parts: list[str]) -> str:
    return " ".join(piece.strip() for piece in parts if piece and piece.strip())


def normalize_segments(segments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "start": s.get("start"),
            "end": s.get("end"),
            "text": (s.get("text") or "").strip(),
            "speaker": s.get("speaker"),
        }
        for s in segments
    ]
