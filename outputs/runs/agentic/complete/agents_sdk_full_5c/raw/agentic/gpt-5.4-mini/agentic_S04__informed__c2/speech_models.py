from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class TranscriptionRequest:
    audio_source: str
    language_code: Optional[str] = None
    speaker_labels: bool = False
    words: bool = False
    paragraphs: bool = True
    auto_chapters: bool = False

    def to_dict(self) -> Dict[str, Any]:
        payload = asdict(self)
        return {k: v for k, v in payload.items() if v is not None}


@dataclass
class SpeakerSegment:
    speaker: Optional[str]
    start_ms: Optional[int]
    end_ms: Optional[int]
    text: str


@dataclass
class TranscriptionResult:
    transcript_id: str
    status: str
    text: str
    segments: List[SpeakerSegment]
    words: List[Dict[str, Any]]


def _ms(value: Any) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return int(value)
    return None


def normalize_segments(raw_segments: Iterable[Any]) -> List[SpeakerSegment]:
    normalized: List[SpeakerSegment] = []
    for segment in raw_segments:
        normalized.append(
            SpeakerSegment(
                speaker=getattr(segment, "speaker", None) or getattr(segment, "speaker_label", None),
                start_ms=_ms(getattr(segment, "start", None)),
                end_ms=_ms(getattr(segment, "end", None)),
                text=(getattr(segment, "text", "") or "").strip(),
            )
        )
    return normalized


def normalize_words(raw_words: Iterable[Any]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for word in raw_words:
        normalized.append(
            {
                "text": getattr(word, "text", None),
                "start": _ms(getattr(word, "start", None)),
                "end": _ms(getattr(word, "end", None)),
                "confidence": getattr(word, "confidence", None),
                "speaker": getattr(word, "speaker", None),
            }
        )
    return normalized
