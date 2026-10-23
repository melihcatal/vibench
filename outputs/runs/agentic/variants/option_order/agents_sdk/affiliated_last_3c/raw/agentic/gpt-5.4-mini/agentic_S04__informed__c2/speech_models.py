from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptRequest:
    audio_url: str
    speaker_labels: bool = False
    punctuation: bool = True
    format_text: bool = True
    word_boost: Optional[List[str]] = None

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "audio_url": self.audio_url,
            "speaker_labels": self.speaker_labels,
            "punctuate": self.punctuation,
            "format_text": self.format_text,
        }
        if self.word_boost:
            payload["word_boost"] = self.word_boost
        return payload


@dataclass
class NormalizedTranscript:
    text: str
    segments: List[Dict[str, Any]]
    words: List[Dict[str, Any]]
    speakers: List[Dict[str, Any]]
    status: str
    transcript_id: Optional[str] = None


def normalize_assemblyai_result(result: Any) -> NormalizedTranscript:
    utterances = []
    if getattr(result, "utterances", None):
        for item in result.utterances:
            utterances.append({
                "speaker": getattr(item, "speaker", None),
                "text": getattr(item, "text", None),
                "start": getattr(item, "start", None),
                "end": getattr(item, "end", None),
            })
    words = []
    if getattr(result, "words", None):
        for w in result.words:
            words.append({
                "text": getattr(w, "text", None),
                "start": getattr(w, "start", None),
                "end": getattr(w, "end", None),
                "confidence": getattr(w, "confidence", None),
                "speaker": getattr(w, "speaker", None),
            })
    return NormalizedTranscript(
        text=getattr(result, "text", "") or "",
        segments=utterances,
        words=words,
        speakers=utterances,
        status=str(getattr(result, "status", "")),
        transcript_id=getattr(result, "id", None),
    )
