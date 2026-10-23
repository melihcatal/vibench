"""Define local request, response, and normalization helpers for Batch Speech-to-Text."""

from dataclasses import dataclass, field
from typing import List, Optional

import assemblyai as aai


@dataclass
class TranscriptionRequest:
    """Normalized request payload for AssemblyAI batch transcription."""
    audio_url: str
    language_code: str = "en"
    speaker_labels: bool = False
    punctuate: bool = True
    format_text: bool = True
    word_boost: Optional[List[str]] = None
    auto_chapters: bool = False
    extra: dict = field(default_factory=dict)

    def to_assemblyai_config(self) -> aai.TranscriptionConfig:
        """Convert to AssemblyAI TranscriptionConfig."""
        config_kwargs = {
            "language_code": self.language_code,
            "punctuate": self.punctuate,
            "format_text": self.format_text,
        }
        if self.speaker_labels:
            config_kwargs["speaker_labels"] = True
        if self.word_boost:
            config_kwargs["word_boost"] = self.word_boost
        if self.auto_chapters:
            config_kwargs["auto_chapters"] = True
        config_kwargs.update(self.extra)
        return aai.TranscriptionConfig(**config_kwargs)


@dataclass
class TranscriptSegment:
    """Normalized segment from a transcription result."""
    text: str
    start_ms: int
    end_ms: int
    speaker: Optional[str] = None
    confidence: float = 1.0

    @classmethod
    def from_assemblyai_utterance(cls, utterance) -> "TranscriptSegment":
        """Create a TranscriptSegment from an AssemblyAI utterance."""
        return cls(
            text=utterance.text,
            start_ms=utterance.start,
            end_ms=utterance.end,
            speaker=str(utterance.speaker) if utterance.speaker is not None else None,
            confidence=utterance.confidence if hasattr(utterance, 'confidence') else 1.0,
        )

    @classmethod
    def from_assemblyai_word(cls, word) -> "TranscriptSegment":
        """Create a TranscriptSegment from an AssemblyAI word object."""
        return cls(
            text=word.text,
            start_ms=word.start,
            end_ms=word.end,
            confidence=word.confidence,
        )


@dataclass
class TranscriptionResponse:
    """Normalized response for a completed transcription job."""
    job_id: str
    text: str
    segments: List[TranscriptSegment] = field(default_factory=list)
    words: List[TranscriptSegment] = field(default_factory=list)
    language: str = "en"
    audio_duration_ms: int = 0
    status: str = "completed"

    @classmethod
    def from_assemblyai_transcript(cls, transcript: aai.Transcript) -> "TranscriptionResponse":
        """Build a TranscriptionResponse from an AssemblyAI Transcript."""
        segments = []
        for utterance in transcript.utterances or []:
            segments.append(TranscriptSegment.from_assemblyai_utterance(utterance))

        words = []
        for word_obj in transcript.words or []:
            words.append(TranscriptSegment.from_assemblyai_word(word_obj))

        return cls(
            job_id=transcript.id,
            text=transcript.text or "",
            segments=segments,
            words=words,
            language=transcript.language_code or "en",
            audio_duration_ms=transcript.audio_duration or 0,
            status=transcript.status.value if transcript.status else "unknown",
        )


def merge_segments(segments: List[TranscriptSegment]) -> str:
    """Merge a list of normalized segments into a single text block."""
    return " ".join(s.text for s in segments if s.text)


def group_segments_by_speaker(segments: List[TranscriptSegment]) -> dict:
    """Group segments by speaker label."""
    speaker_groups = {}
    for seg in segments:
        key = seg.speaker or "unknown"
        if key not in speaker_groups:
            speaker_groups[key] = []
        speaker_groups[key].append(seg)
    return speaker_groups
