from dataclasses import dataclass
from typing import Optional, List, Dict, Any
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
    metadata: Optional[Dict[str, str]] = None


@dataclass
class TranscriptionJob:
    """Model for transcription job status."""

    job_id: str
    status: str  # QUEUED, IN_PROGRESS, COMPLETED, FAILED
    language_code: str
    audio_file: str
    created_at: Optional[datetime] = None
    transcript_uri: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class TranscriptionResult:
    """Model for transcription results."""

    job_id: str
    status: str
    transcript_text: str
    segments: List["TranscriptSegment"]
    language_code: str
    completed_at: Optional[datetime] = None
    confidence_score: Optional[float] = None


@dataclass
class TranscriptSegment:
    """Model for individual transcript segments."""

    text: str
    start_time: float
    end_time: float
    confidence: float


@dataclass
class TimestampedWord:
    """Model for word-level timestamps."""

    word: str
    start_time: float
    end_time: float
    confidence: float


@dataclass
class TimestampedSegment:
    """Model for segment-level timestamps."""

    text: str
    start_time: float
    end_time: float
    word_count: int


@dataclass
class DiarizationRequest:
    """Request model for speaker diarization."""

    audio_file_path: str
    max_speakers: int = 2
    enable_channel_identification: bool = False


@dataclass
class DiarizedSegment:
    """Model for diarized speech segments."""

    speaker_label: str
    text: str
    start_time: float
    end_time: float


@dataclass
class NormalizedTranscript:
    """Normalized transcript for consistent processing."""

    text: str
    segments: List[TranscriptSegment]
    metadata: Dict[str, Any]
    language: str
    duration_seconds: float


def normalize_transcript_data(raw_data: Dict[str, Any]) -> NormalizedTranscript:
    """
    Normalize AWS Transcribe transcript data to consistent format.

    Args:
        raw_data: Raw transcript JSON from AWS Transcribe

    Returns:
        Normalized transcript object
    """
    transcript_text = ""
    segments = []
    duration = 0.0

    if "results" in raw_data:
        transcripts = raw_data["results"].get("transcripts", [])
        if transcripts:
            transcript_text = transcripts[0].get("transcript", "")

        if "items" in raw_data["results"]:
            for item in raw_data["results"]["items"]:
                if item["type"] == "pronunciation":
                    segment = TranscriptSegment(
                        text=item["alternatives"][0]["content"],
                        start_time=float(item["start_time"]),
                        end_time=float(item["end_time"]),
                        confidence=float(
                            item["alternatives"][0].get("confidence", 0.0)
                        ),
                    )
                    segments.append(segment)
                    duration = max(duration, float(item["end_time"]))

    metadata = {
        "source": "aws_transcribe",
        "has_speaker_labels": "speaker_labels" in raw_data.get("results", {}),
        "item_count": len(segments),
    }

    return NormalizedTranscript(
        text=transcript_text,
        segments=segments,
        metadata=metadata,
        language=raw_data.get("results", {}).get("language_code", "en-US"),
        duration_seconds=duration,
    )


def split_into_chunks(
    transcript: NormalizedTranscript, max_chunk_size: int = 1000
) -> List[str]:
    """
    Split transcript text into chunks for processing.

    Args:
        transcript: Normalized transcript
        max_chunk_size: Maximum characters per chunk

    Returns:
        List of text chunks
    """
    if len(transcript.text) <= max_chunk_size:
        return [transcript.text]

    chunks = []
    current_chunk = ""

    for segment in transcript.segments:
        segment_text = segment.text

        if len(current_chunk) + len(segment_text) + 1 <= max_chunk_size:
            current_chunk += " " + segment_text if current_chunk else segment_text
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = segment_text

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
