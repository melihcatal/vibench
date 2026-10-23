from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptWord:
    text: str
    start: Optional[int] = None
    end: Optional[int] = None
    speaker: Optional[str] = None

    @classmethod
    def from_assemblyai(cls, payload: Any) -> "TranscriptWord":
        return cls(
            text=getattr(payload, "text", "") or "",
            start=getattr(payload, "start", None),
            end=getattr(payload, "end", None),
            speaker=getattr(payload, "speaker", None),
        )


@dataclass
class TranscriptionJob:
    id: str
    status: str
    text: str = ""
    language_code: Optional[str] = None
    speaker_labels: bool = False
    words: List[TranscriptWord] = field(default_factory=list)

    @classmethod
    def from_assemblyai(cls, transcript: Any) -> "TranscriptionJob":
        words = [TranscriptWord.from_assemblyai(w) for w in getattr(transcript, "words", []) or []]
        return cls(
            id=str(getattr(transcript, "id", "")),
            status=str(getattr(transcript, "status", "")),
            text=str(getattr(transcript, "text", "") or ""),
            language_code=getattr(transcript, "language_code", None),
            speaker_labels=bool(getattr(transcript, "speaker_labels", False)),
            words=words,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "status": self.status,
            "text": self.text,
            "language_code": self.language_code,
            "speaker_labels": self.speaker_labels,
            "words": [w.__dict__ for w in self.words],
        }


@dataclass
class SubmitTranscriptionRequest:
    source: Any
    language_code: Optional[str] = None
    diarization: bool = False
    word_timestamps: bool = False

    def to_assemblyai_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"speaker_labels": self.diarization, "word_boost": []}
        if isinstance(self.source, str) and self.source.startswith("http"):
            payload["audio_url"] = self.source
        else:
            payload["audio_file"] = self.source
        if self.language_code:
            payload["language_code"] = self.language_code
        if self.word_timestamps:
            payload["word_timestamps"] = True
        return payload
