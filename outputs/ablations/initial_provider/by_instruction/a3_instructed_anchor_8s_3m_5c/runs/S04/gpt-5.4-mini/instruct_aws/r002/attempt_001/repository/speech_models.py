from dataclasses import dataclass, field
from typing import Any


@dataclass
class TranscriptionRequest:
    media_uri: str
    job_name: str
    language_code: str = "en-US"
    vocab_filter_method: str | None = None
    settings: dict[str, Any] = field(default_factory=dict)


@dataclass
class TranscriptSegment:
    start_time: float | None
    end_time: float | None
    speaker_label: str | None
    text: str


def extract_transcript_text(transcript_data: dict[str, Any]) -> str:
    results = transcript_data.get("results", {})
    items = results.get("items", [])
    texts: list[str] = []
    for item in items:
        alternatives = item.get("alternatives", [])
        if alternatives:
            texts.append(alternatives[0].get("content", ""))
    return " ".join(t for t in texts if t).strip()


def normalize_segments(transcript_data: dict[str, Any]) -> list[TranscriptSegment]:
    segments: list[TranscriptSegment] = []
    for segment in transcript_data.get("results", {}).get("speaker_labels", {}).get("segments", []):
        items = segment.get("items", [])
        text = " ".join(item.get("content", "") for item in items).strip()
        segments.append(
            TranscriptSegment(
                start_time=float(segment.get("start_time")) if segment.get("start_time") is not None else None,
                end_time=float(segment.get("end_time")) if segment.get("end_time") is not None else None,
                speaker_label=segment.get("speaker_label"),
                text=text,
            )
        )
    return segments
