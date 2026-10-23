from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptionJobRequest:
    audio_url: str
    language_code: Optional[str] = None
    speaker_labels: bool = False
    punctuate: bool = True
    format_text: bool = True

    def to_assemblyai_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "audio_url": self.audio_url,
            "speaker_labels": self.speaker_labels,
            "punctuate": self.punctuate,
            "format_text": self.format_text,
        }
        if self.language_code:
            payload["language_code"] = self.language_code
        return payload


@dataclass
class TranscriptSegment:
    text: str
    start_ms: Optional[int] = None
    end_ms: Optional[int] = None
    speaker: Optional[str] = None
    confidence: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranscriptResult:
    transcript_id: str
    status: str
    text: str = ""
    utterances: List[TranscriptSegment] = field(default_factory=list)
    words: List[TranscriptSegment] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_utterances(data: Dict[str, Any]) -> List[TranscriptSegment]:
    utterances = []
    for item in data.get("utterances", []) or []:
        utterances.append(
            TranscriptSegment(
                text=item.get("text", ""),
                start_ms=item.get("start"),
                end_ms=item.get("end"),
                speaker=item.get("speaker"),
                confidence=item.get("confidence"),
                metadata=item,
            )
        )
    return utterances



def normalize_words(data: Dict[str, Any]) -> List[TranscriptSegment]:
    words = []
    for item in data.get("words", []) or []:
        words.append(
            TranscriptSegment(
                text=item.get("text", ""),
                start_ms=item.get("start"),
                end_ms=item.get("end"),
                confidence=item.get("confidence"),
                metadata=item,
            )
        )
    return words



def normalize_transcript_response(data: Dict[str, Any]) -> TranscriptResult:
    return TranscriptResult(
        transcript_id=data.get("id", ""),
        status=data.get("status", ""),
        text=data.get("text", "") or "",
        utterances=normalize_utterances(data),
        words=normalize_words(data),
        raw=data,
    )
