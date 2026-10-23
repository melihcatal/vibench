"""
Define local request, response, and normalization helpers for Batch Speech-to-Text.

Provider: Google Cloud Speech-to-Text API
SDK: google-cloud-speech
Model IDs: long, short, phone_call, medical_dictation, medical_conversation
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum


class SpeechModel(str, Enum):
    """Google Cloud Speech-to-Text model identifiers."""
    LONG = "long"
    SHORT = "short"
    PHONE_CALL = "phone_call"
    MEDICAL_DICTATION = "medical_dictation"
    MEDICAL_CONVERSATION = "medical_conversation"


class AudioEncoding(str, Enum):
    """Supported audio encodings for Google Cloud Speech-to-Text."""
    LINEAR16 = "LINEAR16"
    MP3 = "MP3"
    FLAC = "FLAC"
    MULAW = "MULAW"
    AMR = "AMR"
    AMR_WB = "AMR_WB"
    OGG_OPUS = "OGG_OPUS"
    SPEEX_WITH_HEADER_BYTE = "SPEEX_WITH_HEADER_BYTE"


@dataclass
class BatchTranscriptionRequest:
    """Request model for submitting a batch transcription job."""
    gcs_uri: str
    language_code: str = "en-US"
    model: SpeechModel = SpeechModel.LONG
    enable_diarization: bool = False
    enable_word_time_offsets: bool = False
    min_speaker_count: int = 2
    max_speaker_count: int = 6
    output_gcs_uri: Optional[str] = None
    alternative_count: int = 1


@dataclass
class WordTimestamp:
    """Word-level timestamp information."""
    word: str
    start_offset_seconds: float
    end_offset_seconds: float
    speaker_tag: Optional[int] = None
    confidence: Optional[float] = None


@dataclass
class TranscriptSegment:
    """A segment of transcribed speech."""
    transcript: str
    confidence: float
    words: List[WordTimestamp] = field(default_factory=list)
    speaker_tag: Optional[int] = None
    language_code: Optional[str] = None


@dataclass
class BatchTranscriptionResponse:
    """Normalized response from a batch transcription job."""
    job_id: str
    status: str
    results: List[TranscriptSegment] = field(default_factory=list)
    total_segments: int = 0
    has_diarization: bool = False
    has_word_timestamps: bool = False
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class DiarizedSpeaker:
    """Speaker identification from diarization."""
    speaker_tag: int
    total_segments: int
    total_duration_seconds: float
    segments: List[TranscriptSegment] = field(default_factory=list)


@dataclass
class DiarizedTranscript:
    """Transcript organized by speaker."""
    speakers: List[DiarizedSpeaker] = field(default_factory=list)
    full_transcript: str = ""
    speaker_turns: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class TimestampedSegment:
    """A segment with precise word-level timing."""
    segment_id: int
    transcript: str
    words: List[WordTimestamp]
    start_time_seconds: float
    end_time_seconds: float
    confidence: float


def normalize_google_results_to_segments(results) -> List[TranscriptSegment]:
    """
    Convert Google Cloud Speech-to-Text results to TranscriptSegment list.
    """
    segments = []
    for result in results:
        for alternative in result.alternatives:
            words = []
            if alternative.words:
                for word_info in alternative.words:
                    speaker_tag = None
                    if hasattr(word_info, "speaker_tag") and word_info.speaker_tag:
                        speaker_tag = word_info.speaker_tag

                    word_ts = WordTimestamp(
                        word=word_info.word,
                        start_offset_seconds=(
                            word_info.start_offset.seconds
                            + word_info.start_offset.microseconds / 1_000_000
                        ),
                        end_offset_seconds=(
                            word_info.end_offset.seconds
                            + word_info.end_offset.microseconds / 1_000_000
                        ),
                        speaker_tag=speaker_tag,
                        confidence=getattr(word_info, "confidence", None),
                    )
                    words.append(word_ts)

            segment = TranscriptSegment(
                transcript=alternative.transcript,
                confidence=alternative.confidence,
                words=words,
                speaker_tag=words[0].speaker_tag if words else None,
                language_code=getattr(result, "language_code", None),
            )
            segments.append(segment)

    return segments


def build_diarized_transcript(segments: List[TranscriptSegment]) -> DiarizedTranscript:
    """
    Group transcript segments by speaker tag for diarized output.
    """
    speaker_map: Dict[int, DiarizedSpeaker] = {}

    for seg in segments:
        tag = seg.speaker_tag or 0
        if tag not in speaker_map:
            speaker_map[tag] = DiarizedSpeaker(
                speaker_tag=tag,
                total_segments=0,
                total_duration_seconds=0.0,
            )

        speaker = speaker_map[tag]
        speaker.total_segments += 1
        speaker.segments.append(seg)

        if seg.words:
            duration = seg.words[-1].end_offset_seconds - seg.words[0].start_offset_seconds
            speaker.total_duration_seconds += duration

    diarized = DiarizedTranscript(
        speakers=list(speaker_map.values()),
        speaker_turns=[
            {
                "speaker_tag": seg.speaker_tag or 0,
                "transcript": seg.transcript,
                "word_count": len(seg.words),
            }
            for seg in segments
        ],
    )

    full_parts = []
    for seg in segments:
        prefix = f"[Speaker {seg.speaker_tag or 0}] " if seg.speaker_tag else ""
        full_parts.append(f"{prefix}{seg.transcript}")
    diarized.full_transcript = " ".join(full_parts)

    return diarized


def build_timestamped_segments(segments: List[TranscriptSegment]) -> List[TimestampedSegment]:
    """
    Create TimestampedSegment objects with computed start/end times.
    """
    timestamped = []
    for idx, seg in enumerate(segments):
        if not seg.words:
            continue

        start_time = seg.words[0].start_offset_seconds
        end_time = seg.words[-1].end_offset_seconds

        ts = TimestampedSegment(
            segment_id=idx,
            transcript=seg.transcript,
            words=seg.words,
            start_time_seconds=start_time,
            end_time_seconds=end_time,
            confidence=seg.confidence,
        )
        timestamped.append(ts)

    return timestamped
