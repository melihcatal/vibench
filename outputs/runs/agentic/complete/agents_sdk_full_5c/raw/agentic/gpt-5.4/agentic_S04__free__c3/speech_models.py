from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptionSubmission:
    audio_url: str
    language_code: Optional[str] = None
    speaker_labels: bool = False
    word_boost: List[str] = field(default_factory=list)

    def to_assemblyai_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "audio_url": self.audio_url,
            "speaker_labels": self.speaker_labels,
        }
        if self.language_code:
            payload["language_code"] = self.language_code
        if self.word_boost:
            payload["word_boost"] = self.word_boost
        return payload


@dataclass
class TranscriptStatus:
    transcript_id: str
    status: str
    text: str = ""
    error: Optional[str] = None
    utterances: List[Dict[str, Any]] = field(default_factory=list)
    words: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_assemblyai(cls, payload: Dict[str, Any]) -> "TranscriptStatus":
        return cls(
            transcript_id=payload.get("id", ""),
            status=payload.get("status", "unknown"),
            text=payload.get("text", "") or "",
            error=payload.get("error"),
            utterances=payload.get("utterances") or [],
            words=payload.get("words") or [],
        )


def normalize_segments(transcript_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    utterances = transcript_payload.get("utterances") or []
    if utterances:
        return [
            {
                "speaker": item.get("speaker"),
                "start_ms": item.get("start"),
                "end_ms": item.get("end"),
                "text": item.get("text", ""),
            }
            for item in utterances
        ]

    words = transcript_payload.get("words") or []
    segments: List[Dict[str, Any]] = []
    for word in words:
        segments.append(
            {
                "speaker": word.get("speaker"),
                "start_ms": word.get("start"),
                "end_ms": word.get("end"),
                "text": word.get("text", ""),
                "confidence": word.get("confidence"),
            }
        )
    return segments


def transcript_text_from_segments(segments: List[Dict[str, Any]]) -> str:
    return " ".join(segment.get("text", "").strip() for segment in segments if segment.get("text"))
