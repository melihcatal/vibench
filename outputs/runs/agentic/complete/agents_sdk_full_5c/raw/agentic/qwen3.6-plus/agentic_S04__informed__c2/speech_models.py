"""
Local request, response, and normalization helpers for Batch Speech-to-Text.
Defines dataclasses for transcript requests, responses, and utility functions
for normalizing AssemblyAI transcription output.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import datetime


@dataclass
class TranscriptRequest:
    """Normalized request model for a batch transcription job."""
    audio_source: str  # URL or file path
    language_code: str = "en"
    speaker_diarization: bool = False
    word_timestamps: bool = False
    auto_chapters: bool = False
    content_safety: bool = False
    entity_detection: bool = False
    sentiment_analysis: bool = False
    word_boost: Optional[List[str]] = None
    custom_spelling: Optional[Dict[str, str]] = None
    dual_channel: bool = False
    punctuate: bool = True
    format_text: bool = True

    def to_assemblyai_config(self) -> dict:
        """
        Convert to AssemblyAI TranscriptConfig-compatible dict.

        Returns:
            Dictionary of parameters for assemblyai.TranscriptConfig.
        """
        config = {
            "audio_url": self.audio_source,
            "language_code": self.language_code,
            "speaker_labels": self.speaker_diarization,
            "word_boost": self.word_boost,
            "dual_channel": self.dual_channel,
            "punctuate": self.punctuate,
            "format_text": self.format_text,
        }
        if self.auto_chapters:
            config["auto_chapters"] = True
        if self.content_safety:
            config["content_safety"] = True
        if self.entity_detection:
            config["entity_detection"] = True
        if self.sentiment_analysis:
            config["sentiment_analysis"] = True
        if self.custom_spelling:
            config["custom_spelling"] = self.custom_spelling
        return config


@dataclass
class WordSegment:
    """Normalized word-level segment with timing information."""
    text: str
    start_ms: int
    end_ms: int
    confidence: float = 0.0
    speaker: Optional[str] = None
    is_punctuated: bool = True


@dataclass
class Utterance:
    """Normalized speaker utterance with word segments."""
    speaker: Optional[str]
    text: str
    words: List[WordSegment] = field(default_factory=list)
    start_ms: Optional[int] = None
    end_ms: Optional[int] = None
    confidence: float = 0.0
    sentiment: Optional[str] = None


@dataclass
class TranscriptResponse:
    """Normalized transcript response with structured access to results."""
    transcript_id: str
    audio_url: str
    full_text: str
    utterances: List[Utterance] = field(default_factory=list)
    words: List[WordSegment] = field(default_factory=list)
    chapters: Optional[List[dict]] = None
    content_safety_labels: Optional[List[dict]] = None
    entities: Optional[List[dict]] = None
    summary: Optional[str] = None
    status: str = "completed"
    language_code: str = "en"
    duration_ms: int = 0
    created_at: Optional[datetime.datetime] = None
    processing_errors: Optional[str] = None

    def get_full_text(self) -> str:
        """Return the full transcript text."""
        return self.full_text

    def get_speakers(self) -> List[str]:
        """Return unique speaker identifiers."""
        speakers = set()
        for u in self.utterances:
            if u.speaker:
                speakers.add(u.speaker)
        return sorted(speakers)

    def get_utterances_by_speaker(self, speaker: str) -> List[Utterance]:
        """Return all utterances for a specific speaker."""
        return [u for u in self.utterances if u.speaker == speaker]

    def to_dict(self) -> Dict[str, Any]:
        """Serialize response to dictionary."""
        return {
            "transcript_id": self.transcript_id,
            "audio_url": self.audio_url,
            "full_text": self.full_text,
            "utterances": [
                {
                    "speaker": u.speaker,
                    "text": u.text,
                    "start_ms": u.start_ms,
                    "end_ms": u.end_ms,
                    "confidence": u.confidence,
                    "sentiment": u.sentiment,
                }
                for u in self.utterances
            ],
            "words": [
                {
                    "text": w.text,
                    "start_ms": w.start_ms,
                    "end_ms": w.end_ms,
                    "confidence": w.confidence,
                    "speaker": w.speaker,
                }
                for w in self.words
            ],
            "chapters": self.chapters,
            "content_safety_labels": self.content_safety_labels,
            "entities": self.entities,
            "summary": self.summary,
            "status": self.status,
            "language_code": self.language_code,
            "duration_ms": self.duration_ms,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


def normalize_assemblyai_response(raw_transcript) -> TranscriptResponse:
    """
    Normalize an AssemblyAI transcript object into a TranscriptResponse.

    Args:
        raw_transcript: assemblyai.Transcript object from the SDK.

    Returns:
        Normalized TranscriptResponse with structured data.
    """
    response = TranscriptResponse(
        transcript_id=raw_transcript.id,
        audio_url=raw_transcript.audio_url,
        full_text=raw_transcript.text or "",
        status=raw_transcript.status.value if hasattr(raw_transcript.status, "value") else str(raw_transcript.status),
        language_code=raw_transcript.language_code or "en",
        duration_ms=raw_transcript.audio_duration * 1000 if raw_transcript.audio_duration else 0,
    )

    # Normalize words with optional timestamps
    if raw_transcript.words:
        for w in raw_transcript.words:
            word_seg = WordSegment(
                text=w.text,
                start_ms=w.start,
                end_ms=w.end,
                confidence=w.confidence,
            )
            response.words.append(word_seg)

    # Normalize utterances / speaker labels
    if raw_transcript.utterances:
        for u in raw_transcript.utterances:
            utterance = Utterance(
                speaker=u.speaker,
                text=u.text,
                start_ms=u.start,
                end_ms=u.end,
                confidence=u.confidence if hasattr(u, "confidence") else 0.0,
            )
            # Collect word segments for this utterance
            if u.words:
                for w in u.words:
                    utterance.words.append(
                        WordSegment(
                            text=w.text,
                            start_ms=w.start,
                            end_ms=w.end,
                            confidence=w.confidence,
                            speaker=u.speaker,
                        )
                    )
            response.utterances.append(utterance)

    # Normalize chapters if available
    if raw_transcript.chapters:
        response.chapters = [
            {"headline": c.headline, "summary": c.summary, "gist": c.gist}
            for c in raw_transcript.chapters
        ]

    # Normalize content safety labels
    if raw_transcript.content_safety_labels:
        response.content_safety_labels = [
            {
                "text": label.text,
                "labels": label.labels,
                "severity": label.severity,
            }
            for label in raw_transcript.content_safety_labels
        ]

    # Normalize entities
    if raw_transcript.entities:
        response.entities = [
            {"entity_type": e.entity_type, "text": e.text, "start_char": e.start, "end_char": e.end}
            for e in raw_transcript.entities
        ]

    return response


def merge_word_segments(
    words: List[WordSegment], max_duration_ms: int = 3000
) -> List[WordSegment]:
    """
    Merge consecutive word segments into phrase-level segments.

    Args:
        words: List of WordSegment objects.
        max_duration_ms: Maximum duration for a merged segment.

    Returns:
        List of merged WordSegment objects representing phrases.
    """
    if not words:
        return []

    merged = []
    current_text = words[0].text
    current_start = words[0].start_ms
    current_end = words[0].end_ms
    current_speaker = words[0].speaker

    for word in words[1:]:
        segment_duration = word.end_ms - current_start
        if segment_duration > max_duration_ms:
            merged.append(
                WordSegment(
                    text=current_text.strip(),
                    start_ms=current_start,
                    end_ms=current_end,
                    speaker=current_speaker,
                )
            )
            current_text = word.text
            current_start = word.start_ms
            current_end = word.end_ms
            current_speaker = word.speaker
        else:
            current_text += " " + word.text
            current_end = word.end_ms

    # Append final segment
    merged.append(
        WordSegment(
            text=current_text.strip(),
            start_ms=current_start,
            end_ms=current_end,
            speaker=current_speaker,
        )
    )

    return merged


def split_into_sentences(text: str) -> List[str]:
    """
    Simple sentence splitter for transcript text.

    Args:
        text: Full transcript text.

    Returns:
        List of sentence strings.
    """
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in sentences if s]
