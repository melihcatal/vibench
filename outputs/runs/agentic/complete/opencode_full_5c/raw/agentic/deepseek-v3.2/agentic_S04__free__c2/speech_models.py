from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class TranscriptionRequest:
    """Request model for transcription submission."""

    audio_file_path: str
    language_code: str = "en-US"
    enable_speaker_diarization: bool = False
    max_speakers: int = 2
    enable_word_timestamps: bool = True
    custom_vocabulary: Optional[List[str]] = None


@dataclass
class TranscriptionResult:
    """Result model for transcription."""

    job_id: str
    transcript: str
    items: List[Dict[str, Any]]
    speaker_labels: List[Dict[str, Any]]
    status: str
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class DiarizationRequest:
    """Request model for speaker diarization."""

    audio_file_path: str
    max_speakers: int = 2
    language_code: str = "en-US"
    enable_word_level: bool = False


@dataclass
class TimestampedTranscript:
    """Model for timestamped transcript."""

    job_id: str
    word_timestamps: List[Dict[str, Any]]
    segment_timestamps: List[Dict[str, Any]]
    full_transcript: str


def normalize_transcript_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Normalize transcript items for consistent formatting.

    Args:
        items: Raw transcript items from AWS Transcribe

    Returns:
        Normalized items
    """
    normalized = []

    for item in items:
        if item["type"] == "pronunciation":
            normalized.append(
                {
                    "type": "word",
                    "content": item["alternatives"][0]["content"],
                    "start_time": float(item["start_time"]),
                    "end_time": float(item["end_time"]),
                    "confidence": float(item["alternatives"][0].get("confidence", 0.0)),
                }
            )
        elif item["type"] == "punctuation":
            normalized.append(
                {"type": "punctuation", "content": item["alternatives"][0]["content"]}
            )

    return normalized


def parse_speaker_labels(
    speaker_labels: List[Dict[str, Any]],
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Parse speaker labels into organized structure.

    Args:
        speaker_labels: Raw speaker labels from AWS Transcribe

    Returns:
        Dictionary mapping speaker labels to their segments
    """
    speakers = {}

    for segment in speaker_labels:
        speaker_label = segment["speaker_label"]
        if speaker_label not in speakers:
            speakers[speaker_label] = []

        speakers[speaker_label].append(
            {
                "start_time": float(segment["start_time"]),
                "end_time": float(segment["end_time"]),
                "items_count": len(segment.get("items", [])),
            }
        )

    return speakers


def calculate_transcript_metrics(
    transcript: str, items: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Calculate metrics for a transcript.

    Args:
        transcript: Full transcript text
        items: Word-level items

    Returns:
        Dictionary of metrics
    """
    word_items = [item for item in items if item.get("type") == "word"]

    return {
        "word_count": len(word_items),
        "character_count": len(transcript),
        "average_confidence": sum(item.get("confidence", 0) for item in word_items)
        / len(word_items)
        if word_items
        else 0,
        "duration_seconds": max(item.get("end_time", 0) for item in word_items)
        if word_items
        else 0,
    }
