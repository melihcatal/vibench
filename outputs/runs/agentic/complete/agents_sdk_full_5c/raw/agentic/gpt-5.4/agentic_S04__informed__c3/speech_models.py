from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class BatchTranscriptionRequest:
    audio_url: str
    language_code: Optional[str] = None
    speaker_labels: bool = False
    speakers_expected: Optional[int] = None
    punctuate: bool = True
    format_text: bool = True
    webhook_url: Optional[str] = None

    def to_assemblyai_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "audio_url": self.audio_url,
            "punctuate": self.punctuate,
            "format_text": self.format_text,
        }
        if self.language_code:
            payload["language_code"] = self.language_code
        if self.speaker_labels:
            payload["speaker_labels"] = True
        if self.speakers_expected:
            payload["speakers_expected"] = self.speakers_expected
        if self.webhook_url:
            payload["webhook_url"] = self.webhook_url
        return payload


@dataclass
class TranscriptSegment:
    text: str
    start_ms: Optional[int] = None
    end_ms: Optional[int] = None
    speaker: Optional[str] = None
    confidence: Optional[float] = None
    words: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class TranscriptResult:
    transcript_id: str
    status: str
    text: str = ""
    confidence: Optional[float] = None
    language_code: Optional[str] = None
    audio_duration_ms: Optional[int] = None
    utterances: List[TranscriptSegment] = field(default_factory=list)
    words: List[Dict[str, Any]] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_assemblyai_transcript(payload: Dict[str, Any]) -> TranscriptResult:
    utterances = [
        TranscriptSegment(
            text=item.get("text", ""),
            start_ms=item.get("start"),
            end_ms=item.get("end"),
            speaker=item.get("speaker"),
            confidence=item.get("confidence"),
            words=item.get("words") or [],
        )
        for item in (payload.get("utterances") or [])
    ]
    return TranscriptResult(
        transcript_id=payload.get("id", ""),
        status=payload.get("status", "queued"),
        text=payload.get("text", "") or "",
        confidence=payload.get("confidence"),
        language_code=payload.get("language_code"),
        audio_duration_ms=payload.get("audio_duration"),
        utterances=utterances,
        words=payload.get("words") or [],
        raw=payload,
    )


def transcript_segments_from_result(result: TranscriptResult) -> List[Dict[str, Any]]:
    if result.utterances:
        return [
            {
                "text": segment.text,
                "start_ms": segment.start_ms,
                "end_ms": segment.end_ms,
                "speaker": segment.speaker,
                "confidence": segment.confidence,
            }
            for segment in result.utterances
        ]
    if result.text:
        return [{"text": result.text, "start_ms": 0, "end_ms": result.audio_duration_ms}]
    return []
