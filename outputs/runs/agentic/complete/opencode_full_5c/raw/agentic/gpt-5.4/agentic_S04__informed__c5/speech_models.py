from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptionJobRequest:
    audio_url: str
    language_code: str = "en_us"
    speaker_labels: bool = False
    speakers_expected: Optional[int] = None
    word_timestamps: bool = True


@dataclass
class TranscriptWord:
    text: str
    start: Optional[int] = None
    end: Optional[int] = None
    confidence: Optional[float] = None
    speaker: Optional[str] = None


@dataclass
class TranscriptSegment:
    text: str
    start: Optional[int] = None
    end: Optional[int] = None
    speaker: Optional[str] = None
    confidence: Optional[float] = None
    words: List[TranscriptWord] = field(default_factory=list)


@dataclass
class TranscriptionJobStatus:
    transcript_id: str
    status: str
    text: str = ""
    confidence: Optional[float] = None
    language_code: Optional[str] = None
    audio_duration: Optional[float] = None
    segments: List[TranscriptSegment] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_assemblyai_word(item: Dict[str, Any]) -> TranscriptWord:
    speaker_value = item.get("speaker")
    speaker = None if speaker_value in (None, "") else str(speaker_value)
    return TranscriptWord(
        text=item.get("text", ""),
        start=item.get("start"),
        end=item.get("end"),
        confidence=item.get("confidence"),
        speaker=speaker,
    )


def normalize_assemblyai_utterance(item: Dict[str, Any]) -> TranscriptSegment:
    return TranscriptSegment(
        text=item.get("text", ""),
        start=item.get("start"),
        end=item.get("end"),
        speaker=item.get("speaker"),
        confidence=item.get("confidence"),
        words=[normalize_assemblyai_word(word) for word in item.get("words", [])],
    )


def normalize_assemblyai_transcript(payload: Dict[str, Any]) -> TranscriptionJobStatus:
    segments: List[TranscriptSegment] = []
    utterances = payload.get("utterances") or []
    if utterances:
        segments = [normalize_assemblyai_utterance(item) for item in utterances]
    else:
        words = [normalize_assemblyai_word(item) for item in payload.get("words", [])]
        if words:
            segments = [
                TranscriptSegment(
                    text=payload.get("text", ""),
                    start=words[0].start,
                    end=words[-1].end,
                    confidence=payload.get("confidence"),
                    words=words,
                )
            ]
    return TranscriptionJobStatus(
        transcript_id=payload.get("id", ""),
        status=payload.get("status", "queued"),
        text=payload.get("text", "") or "",
        confidence=payload.get("confidence"),
        language_code=payload.get("language_code"),
        audio_duration=payload.get("audio_duration"),
        segments=segments,
        raw=payload,
    )


def transcript_text_from_segments(segments: List[TranscriptSegment]) -> str:
    return "\n".join(segment.text for segment in segments if segment.text).strip()
