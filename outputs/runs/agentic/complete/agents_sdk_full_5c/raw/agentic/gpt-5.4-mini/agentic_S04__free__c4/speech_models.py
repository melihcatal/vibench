from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class TranscriptionRequest:
    audio_path: str
    model: str
    prompt: Optional[str] = None
    language: Optional[str] = None
    timestamp_granularities: Optional[List[str]] = None
    diarize: bool = False

    def to_kwargs(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"model": self.model}
        if self.prompt:
            payload["prompt"] = self.prompt
        if self.language:
            payload["language"] = self.language
        if self.timestamp_granularities:
            payload["timestamp_granularities"] = self.timestamp_granularities
        if self.diarize:
            payload["diarize"] = True
        return payload


@dataclass
class NormalizedSegment:
    start: Optional[float]
    end: Optional[float]
    text: str
    speaker: Optional[str] = None
    words: Optional[List[Dict[str, Any]]] = None


@dataclass
class NormalizedTranscript:
    text: str
    segments: List[NormalizedSegment]
    raw: Any


def _segment_from_any(item: Any) -> NormalizedSegment:
    if isinstance(item, dict):
        return NormalizedSegment(
            start=item.get("start"),
            end=item.get("end"),
            text=item.get("text", ""),
            speaker=item.get("speaker") or item.get("speaker_id"),
            words=item.get("words"),
        )
    return NormalizedSegment(start=getattr(item, "start", None), end=getattr(item, "end", None), text=getattr(item, "text", ""), speaker=getattr(item, "speaker", None), words=getattr(item, "words", None))


def normalize_transcript(result: Any) -> NormalizedTranscript:
    text = getattr(result, "text", None) or (result.get("text") if isinstance(result, dict) else "") or ""
    segments: List[NormalizedSegment] = []
    raw_segments: Iterable[Any] = []
    if isinstance(result, dict):
        raw_segments = result.get("segments") or []
    else:
        raw_segments = getattr(result, "segments", []) or []
    for item in raw_segments:
        segments.append(_segment_from_any(item))
    return NormalizedTranscript(text=text, segments=segments, raw=result)
