from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptionSubmission:
    audio_url: str
    language_code: Optional[str] = None
    speaker_labels: bool = False
    speakers_expected: Optional[int] = None
    punctuate: bool = True
    format_text: bool = True

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
        if self.speakers_expected is not None:
            payload["speakers_expected"] = self.speakers_expected
        return payload


@dataclass
class TranscriptSegment:
    start_ms: Optional[int]
    end_ms: Optional[int]
    text: str
    speaker: Optional[str] = None
    confidence: Optional[float] = None
    words: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class TranscriptResult:
    job_id: str
    status: str
    text: str
    language_code: Optional[str] = None
    confidence: Optional[float] = None
    audio_url: Optional[str] = None
    segments: List[TranscriptSegment] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_assemblyai_transcript(transcript: Any) -> TranscriptResult:
    utterances = getattr(transcript, "utterances", None) or []
    words = getattr(transcript, "words", None) or []
    segments: List[TranscriptSegment] = []

    if utterances:
        for utterance in utterances:
            segments.append(
                TranscriptSegment(
                    start_ms=getattr(utterance, "start", None),
                    end_ms=getattr(utterance, "end", None),
                    text=getattr(utterance, "text", "") or "",
                    speaker=(str(getattr(utterance, "speaker", "")) or None),
                    confidence=getattr(utterance, "confidence", None),
                    words=[
                        _word_to_dict(word)
                        for word in getattr(utterance, "words", []) or []
                    ],
                )
            )
    elif words:
        combined = " ".join(
            (getattr(word, "text", "") or "").strip() for word in words
        ).strip()
        if combined:
            segments.append(
                TranscriptSegment(
                    start_ms=getattr(words[0], "start", None),
                    end_ms=getattr(words[-1], "end", None),
                    text=combined,
                    words=[_word_to_dict(word) for word in words],
                )
            )

    return TranscriptResult(
        job_id=getattr(transcript, "id", ""),
        status=getattr(transcript, "status", "unknown"),
        text=getattr(transcript, "text", "") or "",
        language_code=getattr(transcript, "language_code", None),
        confidence=getattr(transcript, "confidence", None),
        audio_url=getattr(transcript, "audio_url", None),
        segments=segments,
        raw=_to_dict(transcript),
    )


def _word_to_dict(word: Any) -> Dict[str, Any]:
    return {
        "text": getattr(word, "text", None),
        "start": getattr(word, "start", None),
        "end": getattr(word, "end", None),
        "confidence": getattr(word, "confidence", None),
        "speaker": getattr(word, "speaker", None),
    }


def _to_dict(value: Any) -> Dict[str, Any]:
    if hasattr(value, "__dict__"):
        result: Dict[str, Any] = {}
        for key, item in value.__dict__.items():
            if key.startswith("_"):
                continue
            result[key] = _convert(item)
        return result
    if isinstance(value, dict):
        return {str(k): _convert(v) for k, v in value.items()}
    return {"value": _convert(value)}


def _convert(value: Any) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, list):
        return [_convert(item) for item in value]
    if isinstance(value, dict):
        return {str(k): _convert(v) for k, v in value.items()}
    if hasattr(value, "__dict__"):
        return {
            k: _convert(v) for k, v in value.__dict__.items() if not k.startswith("_")
        }
    return str(value)
