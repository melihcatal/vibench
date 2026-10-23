"""
Define local request, response, and normalization helpers for Batch Speech-to-Text.

Contains dataclasses for transcription results, status enums, and parsing
utilities for Azure AI Speech batch transcription API responses.
"""

import json
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict


class TranscriptionStatus(str, Enum):
    """Status values returned by Azure AI Speech batch transcription API."""

    NOT_STARTED = "NotStarted"
    RUNNING = "Running"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"

    @classmethod
    def from_string(cls, status_str: str) -> "TranscriptionStatus":
        """
        Convert a raw Azure Speech status string to the enum value.

        Args:
            status_str: Raw status string from Azure API.

        Returns:
            Corresponding TranscriptionStatus enum member.
        """
        mapping = {
            "NotStarted": cls.NOT_STARTED,
            "Running": cls.RUNNING,
            "Succeeded": cls.SUCCEEDED,
            "Failed": cls.FAILED,
        }
        return mapping.get(status_str, cls.NOT_STARTED)


@dataclass
class TranscriptionSegment:
    """A single segment of transcribed text with optional speaker label."""

    text: str
    speaker_label: Optional[str] = None
    start_time_ms: float = 0.0
    end_time_ms: float = 0.0
    confidence: float = 0.0


@dataclass
class TranscriptionResult:
    """
    Normalized transcription result from Azure AI Speech batch API.

    Provides a consistent internal representation regardless of the
    raw JSON structure returned by the Azure Speech service.
    """

    display_text: str = ""
    segments: List[TranscriptionSegment] = field(default_factory=list)
    locale: str = "en-US"
    duration_ms: float = 0.0

    @classmethod
    def from_azure_response(cls, raw_data: dict) -> "TranscriptionResult":
        """
        Parse an Azure AI Speech batch transcription JSON response into a
        normalized TranscriptionResult.

        Azure Speech batch results contain a 'combinedPhrases' array where
        each entry has text, speaker, offset, and duration fields.

        Args:
            raw_data: Raw JSON dict from Azure Speech transcription file.

        Returns:
            Normalized TranscriptionResult instance.
        """
        combined_phrases = raw_data.get("combinedPhrases", [])

        segments = []
        full_text_parts = []

        for phrase in combined_phrases:
            text = phrase.get("text", "")
            speaker = phrase.get("speaker")
            offset = phrase.get("offset", 0)
            duration = phrase.get("duration", 0)

            full_text_parts.append(text)

            segments.append(
                TranscriptionSegment(
                    text=text,
                    speaker_label=speaker,
                    start_time_ms=offset / 10000,
                    end_time_ms=(offset + duration) / 10000,
                )
            )

        display_text = " ".join(full_text_parts).strip()

        return cls(
            display_text=display_text,
            segments=segments,
            locale=raw_data.get("locale", "en-US"),
            duration_ms=segments[-1].end_time_ms if segments else 0.0,
        )

    def to_text(self) -> str:
        """Return the full concatenated transcript text."""
        return self.display_text

    def to_segments_text(self, include_speaker: bool = True) -> str:
        """Return formatted text with optional speaker labels per segment."""
        lines = []
        for seg in self.segments:
            if include_speaker and seg.speaker_label:
                lines.append(f"[{seg.speaker_label}] {seg.text}")
            else:
                lines.append(seg.text)
        return "\n".join(lines)


@dataclass
class TimestampedWord:
    """A single word with start and end timestamps."""

    text: str
    start_time_ms: float
    end_time_ms: float
    confidence: float = 0.0


@dataclass
class TimestampedSegment:
    """A transcript segment (phrase) with word-level timestamps."""

    text: str
    start_time_ms: float
    end_time_ms: float
    words: List[TimestampedWord] = field(default_factory=list)


@dataclass
class TimestampedTranscript:
    """Full transcript with word and segment timing information."""

    words: List[TimestampedWord] = field(default_factory=list)
    segments: List[TimestampedSegment] = field(default_factory=list)
    total_duration_ms: float = 0.0


@dataclass
class SpeakerDiarizationResult:
    """Result containing speaker-labeled transcript segments."""

    segments: List[TranscriptionSegment] = field(default_factory=list)
    speaker_count: int = 0

    def get_speakers(self) -> List[str]:
        """Return list of unique speaker labels."""
        return list(
            set(s.speaker_label for s in self.segments if s.speaker_label is not None)
        )

    def get_segments_by_speaker(self, speaker_label: str) -> List[TranscriptionSegment]:
        """Return all segments spoken by a specific speaker."""
        return [
            s for s in self.segments if s.speaker_label == speaker_label
        ]

    def to_formatted_text(self) -> str:
        """Return a formatted transcript with speaker labels."""
        lines = []
        for seg in self.segments:
            speaker = seg.speaker_label or "Unknown"
            lines.append(f"[{speaker}] {seg.text}")
        return "\n".join(lines)


def normalize_timestamp_ms(raw_offset: int, raw_duration: int = 0) -> Dict[str, float]:
    """
    Convert Azure Speech 100-nanosecond units to milliseconds.

    Azure AI Speech batch transcription returns timing in 100-nanosecond
    increments (1 unit = 0.0001 ms).

    Args:
        raw_offset: Offset in 100ns units.
        raw_duration: Duration in 100ns units.

    Returns:
        Dictionary with start_time_ms and end_time_ms.
    """
    start_ms = raw_offset / 10000.0
    end_ms = (raw_offset + raw_duration) / 10000.0
    return {"start_time_ms": start_ms, "end_time_ms": end_ms}


def build_segment_from_azure_phrase(phrase: dict) -> TranscriptionSegment:
    """
    Build a TranscriptionSegment from a single Azure Speech phrase dict.

    Args:
        phrase: Dictionary from Azure 'combinedPhrases' or 'recognizedPhrases'.

    Returns:
        Normalized TranscriptionSegment.
    """
    text = phrase.get("text", "")
    speaker = phrase.get("speaker")
    offset = phrase.get("offset", 0)
    duration = phrase.get("duration", 0)

    timing = normalize_timestamp_ms(offset, duration)

    return TranscriptionSegment(
        text=text,
        speaker_label=speaker,
        start_time_ms=timing["start_time_ms"],
        end_time_ms=timing["end_time_ms"],
    )
