from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from enum import Enum


class TranscriptionStatus(str, Enum):
    """Status of a transcription job."""

    QUEUED = "QUEUED"
    IN_PROGRESS = "IN_PROGRESS"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"


class MediaFormat(str, Enum):
    """Supported audio formats."""

    MP3 = "mp3"
    MP4 = "mp4"
    WAV = "wav"
    FLAC = "flac"
    OGG = "ogg"
    AMR = "amr"
    WEBM = "webm"


@dataclass
class TranscriptionRequest:
    """Request model for transcription submission."""

    audio_path: str
    language_code: str = "en-US"
    media_format: Optional[str] = None
    enable_diarization: bool = True
    max_speakers: int = 2
    enable_timestamps: bool = True
    custom_vocabulary: Optional[str] = None
    job_name: Optional[str] = None

    def __post_init__(self):
        if self.media_format is None:
            if self.audio_path.startswith("s3://"):
                self.media_format = self.audio_path.split(".")[-1].lower()
            else:
                self.media_format = self.audio_path.split(".")[-1].lower()

            if self.media_format not in [fmt.value for fmt in MediaFormat]:
                self.media_format = MediaFormat.MP3.value


@dataclass
class WordTimestamp:
    """Timestamp information for a single word."""

    word: str
    start_time: float
    end_time: float
    confidence: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "word": self.word,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "confidence": self.confidence,
        }


@dataclass
class SpeakerSegment:
    """Segment of speech from a specific speaker."""

    speaker_label: str
    start_time: float
    end_time: float
    text: str
    words: List[WordTimestamp] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "speaker": self.speaker_label,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "text": self.text,
            "words": [word.to_dict() for word in self.words],
        }


@dataclass
class TranscriptionResult:
    """Complete transcription result."""

    job_name: str
    status: TranscriptionStatus
    transcript_text: str
    language_code: str
    word_timestamps: List[WordTimestamp] = field(default_factory=list)
    speaker_segments: List[SpeakerSegment] = field(default_factory=list)
    raw_response: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

    @classmethod
    def from_amazon_response(
        cls, job_name: str, response_data: Dict[str, Any]
    ) -> "TranscriptionResult":
        """Create TranscriptionResult from Amazon Transcribe response."""
        transcript_text = response_data["results"]["transcripts"][0]["transcript"]

        word_timestamps = []
        speaker_segments = []

        items = response_data["results"].get("items", [])
        speaker_labels = (
            response_data["results"].get("speaker_labels", {}).get("segments", [])
        )

        for item in items:
            if item["type"] == "pronunciation":
                word_timestamps.append(
                    WordTimestamp(
                        word=item["alternatives"][0]["content"],
                        start_time=float(item.get("start_time", 0)),
                        end_time=float(item.get("end_time", 0)),
                        confidence=float(item["alternatives"][0].get("confidence", 0)),
                    )
                )

        for segment in speaker_labels:
            start_time = float(segment["start_time"])
            end_time = float(segment["end_time"])
            speaker_label = segment["speaker_label"]

            segment_words = [
                word
                for word in word_timestamps
                if word.start_time >= start_time and word.end_time <= end_time
            ]

            segment_text = " ".join([word.word for word in segment_words])

            speaker_segments.append(
                SpeakerSegment(
                    speaker_label=speaker_label,
                    start_time=start_time,
                    end_time=end_time,
                    text=segment_text,
                    words=segment_words,
                )
            )

        return cls(
            job_name=job_name,
            status=TranscriptionStatus.COMPLETED,
            transcript_text=transcript_text,
            language_code=response_data.get("language_code", "en-US"),
            word_timestamps=word_timestamps,
            speaker_segments=speaker_segments,
            raw_response=response_data,
        )

    def get_formatted_transcript(
        self, include_speakers: bool = True, include_timestamps: bool = True
    ) -> str:
        """Get formatted transcript text."""
        lines = []

        if include_speakers and self.speaker_segments:
            for segment in self.speaker_segments:
                if include_timestamps:
                    start_min = int(segment.start_time // 60)
                    start_sec = int(segment.start_time % 60)
                    timestamp = f"[{start_min:02d}:{start_sec:02d}]"
                    lines.append(f"{timestamp} {segment.speaker_label}: {segment.text}")
                else:
                    lines.append(f"{segment.speaker_label}: {segment.text}")
        else:
            lines.append(self.transcript_text)

        return "\n".join(lines)

    def get_word_count(self) -> int:
        """Get total word count."""
        return len(self.word_timestamps)

    def get_duration(self) -> float:
        """Get audio duration in seconds."""
        if not self.word_timestamps:
            return 0.0
        return max(word.end_time for word in self.word_timestamps)


def normalize_audio_format(file_path: str) -> str:
    """Normalize audio file format from extension."""
    ext = file_path.split(".")[-1].lower()
    if ext in ["mp3"]:
        return "mp3"
    elif ext in ["wav", "wave"]:
        return "wav"
    elif ext in ["flac"]:
        return "flac"
    elif ext in ["ogg", "oga"]:
        return "ogg"
    elif ext in ["mp4", "m4a"]:
        return "mp4"
    elif ext in ["webm"]:
        return "webm"
    else:
        return "mp3"
