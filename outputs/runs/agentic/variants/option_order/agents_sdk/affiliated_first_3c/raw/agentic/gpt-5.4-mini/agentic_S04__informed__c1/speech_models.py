from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass(frozen=True)
class SpeechSubmission:
    audio_url: str
    speaker_labels: bool = False
    punctuate: bool = True
    timestamps: bool = False

    def to_payload(self) -> Dict[str, Any]:
        return {
            "audio_url": self.audio_url,
            "speaker_labels": self.speaker_labels,
            "punctuate": self.punctuate,
            "timestamps": self.timestamps,
        }


@dataclass(frozen=True)
class TranscriptSegment:
    text: str
    start: Optional[float] = None
    end: Optional[float] = None
    speaker: Optional[str] = None
    words: Optional[List[Dict[str, Any]]] = None


@dataclass(frozen=True)
class NormalizedTranscript:
    text: str
    segments: List[TranscriptSegment]
    raw: Dict[str, Any]


def normalize_words(words: Iterable[Any]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for word in words:
        if isinstance(word, dict):
            normalized.append(
                {
                    "text": word.get("text") or word.get("word") or "",
                    "start": word.get("start"),
                    "end": word.get("end"),
                    "speaker": word.get("speaker"),
                }
            )
        else:
            normalized.append({"text": str(word), "start": None, "end": None, "speaker": None})
    return normalized


def normalize_transcript_result(result: Any) -> NormalizedTranscript:
    raw = getattr(result, "json_response", None) or getattr(result, "dict", lambda: {})()
    text = getattr(result, "text", None) or raw.get("text", "")
    utterances = raw.get("utterances") or []
    segments: List[TranscriptSegment] = []
    for item in utterances:
        segments.append(
            TranscriptSegment(
                text=item.get("text", ""),
                start=item.get("start"),
                end=item.get("end"),
                speaker=item.get("speaker"),
                words=normalize_words(item.get("words", [])),
            )
        )
    return NormalizedTranscript(text=text, segments=segments, raw=raw)
