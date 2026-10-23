from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class AudioSource:
    file_url: str
    content_type: str = "audio/mpeg"
    filename: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = {"file_url": self.file_url, "content_type": self.content_type}
        if self.filename:
            data["filename"] = self.filename
        return data


@dataclass
class TranscriptionRequest:
    audio_url: str
    language_code: Optional[str] = None
    speaker_labels: bool = False
    punctuate: bool = True
    format_text: bool = True
    webhook_url: Optional[str] = None

    def to_assemblyai_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "audio_url": self.audio_url,
            "speaker_labels": self.speaker_labels,
            "punctuate": self.punctuate,
            "format_text": self.format_text,
        }
        if self.language_code:
            payload["language_code"] = self.language_code
        if self.webhook_url:
            payload["webhook_url"] = self.webhook_url
        return payload


@dataclass
class TranscriptSegment:
    start: Optional[float] = None
    end: Optional[float] = None
    speaker: Optional[str] = None
    text: str = ""
    words: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_assemblyai(cls, segment: Dict[str, Any]) -> "TranscriptSegment":
        return cls(
            start=segment.get("start"),
            end=segment.get("end"),
            speaker=segment.get("speaker"),
            text=segment.get("text", ""),
            words=segment.get("words", []) or [],
        )


@dataclass
class TranscriptResult:
    id: str
    status: str
    text: str = ""
    segments: List[TranscriptSegment] = field(default_factory=list)
    error: Optional[str] = None

    @classmethod
    def from_assemblyai(cls, data: Dict[str, Any]) -> "TranscriptResult":
        segments = [TranscriptSegment.from_assemblyai(item) for item in data.get("utterances", []) or []]
        return cls(
            id=str(data.get("id", "")),
            status=str(data.get("status", "")),
            text=data.get("text", "") or "",
            segments=segments,
            error=data.get("error"),
        )


@dataclass
class TranslationRequest:
    source_text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass
class ModerationFinding:
    score: float
    category: str
    reason: Optional[str] = None


@dataclass
class ArchiveSummary:
    title: str
    bullets: List[str]
    summary: str


@dataclass
class EmbeddingBatch:
    items: List[str]

    def __iter__(self) -> Iterable[str]:
        return iter(self.items)
