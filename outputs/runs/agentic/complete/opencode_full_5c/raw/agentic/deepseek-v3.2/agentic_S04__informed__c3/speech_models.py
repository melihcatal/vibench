from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class TranscriptionRequest:
    """Request model for transcription submission."""

    audio_file_path: str
    language_code: str = "en-US"
    enable_speaker_diarization: bool = True
    max_speakers: int = 10
    enable_word_timestamps: bool = True
    custom_vocabulary: Optional[List[str]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranscriptionResult:
    """Result model for completed transcription."""

    job_id: str
    transcript: str
    language_code: str
    speaker_segments: List[Dict[str, Any]] = field(default_factory=list)
    word_timestamps: List[Dict[str, Any]] = field(default_factory=list)
    confidence_score: Optional[float] = None
    duration_seconds: Optional[float] = None
    created_at: datetime = field(default_factory=datetime.now)
    raw_response: Optional[Dict[str, Any]] = None

    def get_speaker_transcript(self, speaker_label: str) -> str:
        """Get transcript for a specific speaker."""
        words_by_speaker = {}
        for word in self.word_timestamps:
            # Find which speaker segment this word belongs to
            for segment in self.speaker_segments:
                if segment["start_time"] <= word["start_time"] <= segment["end_time"]:
                    speaker = segment["speaker_label"]
                    if speaker not in words_by_speaker:
                        words_by_speaker[speaker] = []
                    words_by_speaker[speaker].append(word["word"])
                    break

        if speaker_label in words_by_speaker:
            return " ".join(words_by_speaker[speaker_label])
        return ""


@dataclass
class DiarizationRequest:
    """Request model for speaker diarization."""

    audio_file_path: str
    max_speakers: int = 10
    enable_channel_identification: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DiarizationResult:
    """Result model for speaker diarization."""

    job_id: str
    audio_file: Optional[str] = None
    speaker_segments: List[Dict[str, Any]] = field(default_factory=list)
    total_speakers: int = 0
    status: str = "PENDING"  # PENDING, SUBMITTED, IN_PROGRESS, COMPLETED, FAILED
    error_message: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    raw_response: Optional[Dict[str, Any]] = None

    def get_speaker_timeline(self) -> List[Dict[str, Any]]:
        """Get timeline of speaker changes."""
        timeline = []
        for segment in self.speaker_segments:
            timeline.append(
                {
                    "speaker": segment["speaker_label"],
                    "start_time": segment["start_time"],
                    "end_time": segment["end_time"],
                    "duration": segment["end_time"] - segment["start_time"],
                }
            )
        return timeline


@dataclass
class TimestampedTranscript:
    """Model for timestamped transcript with word and segment timestamps."""

    job_id: str
    word_timestamps: List[Dict[str, Any]]
    segments: List[Dict[str, Any]]
    speaker_segments: List[Dict[str, Any]] = field(default_factory=list)
    full_transcript: Optional[str] = None
    confidence_scores: Optional[List[float]] = None
    raw_response: Optional[Dict[str, Any]] = None

    def get_transcript_with_timestamps(self, format: str = "srt") -> str:
        """Format transcript with timestamps in SRT or VTT format."""
        if format.lower() == "srt":
            return self._format_srt()
        elif format.lower() == "vtt":
            return self._format_vtt()
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _format_srt(self) -> str:
        """Format as SRT subtitles."""
        srt_lines = []
        for i, segment in enumerate(self.segments, 1):
            start_time = self._format_timestamp_srt(segment["start_time"])
            end_time = self._format_timestamp_srt(segment["end_time"])
            srt_lines.append(f"{i}\n{start_time} --> {end_time}\n{segment['text']}\n")
        return "\n".join(srt_lines)

    def _format_vtt(self) -> str:
        """Format as WebVTT subtitles."""
        vtt_lines = ["WEBVTT\n"]
        for i, segment in enumerate(self.segments, 1):
            start_time = self._format_timestamp_vtt(segment["start_time"])
            end_time = self._format_timestamp_vtt(segment["end_time"])
            vtt_lines.append(f"{start_time} --> {end_time}\n{segment['text']}\n")
        return "\n".join(vtt_lines)

    def _format_timestamp_srt(self, seconds: float) -> str:
        """Format seconds as SRT timestamp (HH:MM:SS,mmm)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        milliseconds = int((secs - int(secs)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{int(secs):02d},{milliseconds:03d}"

    def _format_timestamp_vtt(self, seconds: float) -> str:
        """Format seconds as VTT timestamp (HH:MM:SS.mmm)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        milliseconds = int((secs - int(secs)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{int(secs):02d}.{milliseconds:03d}"


def normalize_transcript(transcript: str) -> str:
    """Normalize transcript text."""
    import re

    # Remove extra whitespace
    transcript = re.sub(r"\s+", " ", transcript).strip()

    # Capitalize first letter of sentences
    sentences = re.split(r"([.!?])\s+", transcript)
    normalized = []
    for i in range(0, len(sentences), 2):
        if i < len(sentences):
            sentence = sentences[i].strip()
            if sentence:
                sentence = sentence[0].upper() + sentence[1:]
                normalized.append(sentence)
            if i + 1 < len(sentences):
                normalized.append(sentences[i + 1])

    return " ".join(normalized)


def calculate_confidence_stats(
    word_timestamps: List[Dict[str, Any]],
) -> Dict[str, float]:
    """Calculate confidence statistics from word timestamps."""
    if not word_timestamps:
        return {"mean": 0.0, "min": 0.0, "max": 0.0, "std": 0.0}

    confidences = [
        word["confidence"] for word in word_timestamps if "confidence" in word
    ]

    if not confidences:
        return {"mean": 0.0, "min": 0.0, "max": 0.0, "std": 0.0}

    import statistics

    return {
        "mean": statistics.mean(confidences),
        "min": min(confidences),
        "max": max(confidences),
        "std": statistics.stdev(confidences) if len(confidences) > 1 else 0.0,
    }
