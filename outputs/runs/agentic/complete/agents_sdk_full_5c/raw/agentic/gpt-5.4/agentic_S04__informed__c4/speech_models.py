from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptJob:
    id: str
    status: str
    audio_url: Optional[str] = None
    language_code: Optional[str] = None
    provider: str = "assemblyai"
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranscriptSegment:
    text: str
    start_ms: Optional[int] = None
    end_ms: Optional[int] = None
    speaker: Optional[str] = None
    confidence: Optional[float] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranscriptResult:
    id: str
    status: str
    text: str
    language_code: Optional[str] = None
    segments: List[TranscriptSegment] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationSegment:
    text: str
    translated_text: str
    target_language: str


@dataclass
class ModerationResult:
    flagged: bool
    scores: Dict[str, float]
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingResult:
    text: str
    vector: List[float]
    model: str


@dataclass
class SummaryResult:
    summary: str
    model: str
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_utterances(utterances: Optional[List[Dict[str, Any]]]) -> List[TranscriptSegment]:
    segments: List[TranscriptSegment] = []
    for item in utterances or []:
        segments.append(
            TranscriptSegment(
                text=item.get("text", ""),
                start_ms=item.get("start"),
                end_ms=item.get("end"),
                speaker=item.get("speaker"),
                confidence=item.get("confidence"),
                raw=item,
            )
        )
    return segments


def normalize_words(words: Optional[List[Dict[str, Any]]]) -> List[TranscriptSegment]:
    segments: List[TranscriptSegment] = []
    for item in words or []:
        segments.append(
            TranscriptSegment(
                text=item.get("text") or item.get("word", ""),
                start_ms=item.get("start"),
                end_ms=item.get("end"),
                confidence=item.get("confidence"),
                raw=item,
            )
        )
    return segments


def normalize_sentences(sentences: Optional[List[Dict[str, Any]]]) -> List[TranscriptSegment]:
    segments: List[TranscriptSegment] = []
    for item in sentences or []:
        segments.append(
            TranscriptSegment(
                text=item.get("text", ""),
                start_ms=item.get("start"),
                end_ms=item.get("end"),
                confidence=item.get("confidence"),
                raw=item,
            )
        )
    return segments
