from dataclasses import dataclass, field
from typing import Any


def normalize_segments(segments):
    normalized = []
    for segment in segments or []:
        normalized.append(
            {
                "start": segment.get("start", segment.get("start_time")),
                "end": segment.get("end", segment.get("end_time")),
                "speaker": segment.get("speaker", segment.get("speaker_label")),
                "text": segment.get("text", ""),
                "words": segment.get("words", []),
            }
        )
    return normalized


@dataclass
class TranscriptionRequest:
    audio_uri: str
    language_code: str = "en-US"
    job_name: str | None = None
    diarization: bool = False
    timestamps: bool = False


@dataclass
class TranscriptResponse:
    job_id: str
    status: str
    transcript: str = ""
    segments: list[dict[str, Any]] = field(default_factory=list)
