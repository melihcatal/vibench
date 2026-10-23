from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptionJobRequest:
    audio_url: str
    language_code: Optional[str] = None
    speaker_labels: bool = False
    speakers_expected: Optional[int] = None

    def to_assemblyai_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"audio_url": self.audio_url}
        if self.language_code:
            payload["language_code"] = self.language_code
        if self.speaker_labels:
            payload["speaker_labels"] = True
        if self.speakers_expected is not None:
            payload["speakers_expected"] = self.speakers_expected
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
    segments: List[TranscriptSegment] = field(default_factory=list)
    utterances: List[TranscriptSegment] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


def _segment_from_mapping(item: Dict[str, Any]) -> TranscriptSegment:
    return TranscriptSegment(
        text=item.get("text", ""),
        start_ms=item.get("start"),
        end_ms=item.get("end"),
        speaker=item.get("speaker"),
        confidence=item.get("confidence"),
        words=item.get("words") or [],
    )


def normalize_transcript_response(data: Dict[str, Any]) -> TranscriptResult:
    utterances = [_segment_from_mapping(item) for item in data.get("utterances", [])]
    segments = [_segment_from_mapping(item) for item in data.get("words", [])]
    return TranscriptResult(
        transcript_id=data.get("id", ""),
        status=data.get("status", "unknown"),
        text=data.get("text", "") or "",
        segments=segments,
        utterances=utterances,
        raw=data,
    )


def extract_timestamp_items(data: Dict[str, Any], granularity: str = "word") -> List[Dict[str, Any]]:
    if granularity == "segment":
        source = data.get("utterances") or []
    else:
        source = data.get("words") or []

    items: List[Dict[str, Any]] = []
    for item in source:
        items.append(
            {
                "text": item.get("text", ""),
                "start_ms": item.get("start"),
                "end_ms": item.get("end"),
                "speaker": item.get("speaker"),
                "confidence": item.get("confidence"),
            }
        )
    return items
