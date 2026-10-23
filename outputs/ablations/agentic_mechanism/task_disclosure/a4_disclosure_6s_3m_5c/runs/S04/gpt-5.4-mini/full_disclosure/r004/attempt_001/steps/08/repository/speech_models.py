from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Union


@dataclass(frozen=True)
class SpeechTranscriptRequest:
    audio_url: str
    language_code: Optional[str] = None
    speaker_labels: bool = False
    punctuate: bool = True
    format_text: bool = True
    auto_highlights: bool = False
    sentiment_analysis: bool = False
    entity_detection: bool = False

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "audio_url": self.audio_url,
            "punctuate": self.punctuate,
            "format_text": self.format_text,
            "auto_highlights": self.auto_highlights,
            "sentiment_analysis": self.sentiment_analysis,
            "entity_detection": self.entity_detection,
        }
        if self.language_code:
            payload["language_code"] = self.language_code
        if self.speaker_labels:
            payload["speaker_labels"] = True
        return payload


@dataclass(frozen=True)
class TranscriptWord:
    text: str
    start: Optional[int] = None
    end: Optional[int] = None
    confidence: Optional[float] = None
    speaker: Optional[str] = None


@dataclass(frozen=True)
class TranscriptSegment:
    text: str
    start: Optional[int] = None
    end: Optional[int] = None
    confidence: Optional[float] = None
    speaker: Optional[str] = None
    words: Sequence[TranscriptWord] = field(default_factory=tuple)


@dataclass(frozen=True)
class SpeechTranscriptResponse:
    id: str
    status: str
    text: Optional[str] = None
    audio_url: Optional[str] = None
    language_code: Optional[str] = None
    duration: Optional[int] = None
    error: Optional[str] = None
    raw: Mapping[str, Any] = field(default_factory=dict)


def _coerce_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _coerce_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def normalize_word(word: Mapping[str, Any]) -> TranscriptWord:
    return TranscriptWord(
        text=str(word.get("text", "")),
        start=_coerce_int(word.get("start")),
        end=_coerce_int(word.get("end")),
        confidence=_coerce_float(word.get("confidence")),
        speaker=word.get("speaker"),
    )


def normalize_segment(segment: Mapping[str, Any]) -> TranscriptSegment:
    words = tuple(normalize_word(w) for w in segment.get("words", []) or [])
    return TranscriptSegment(
        text=str(segment.get("text", "")),
        start=_coerce_int(segment.get("start")),
        end=_coerce_int(segment.get("end")),
        confidence=_coerce_float(segment.get("confidence")),
        speaker=segment.get("speaker"),
        words=words,
    )


def normalize_transcript_response(payload: Mapping[str, Any]) -> SpeechTranscriptResponse:
    return SpeechTranscriptResponse(
        id=str(payload.get("id") or payload.get("job_id") or payload.get("transcript_id") or ""),
        status=str(payload.get("status") or payload.get("state") or ""),
        text=payload.get("text") or payload.get("transcript") or payload.get("output_text"),
        audio_url=payload.get("audio_url"),
        language_code=payload.get("language_code"),
        duration=_coerce_int(payload.get("duration")),
        error=payload.get("error") or payload.get("message"),
        raw=payload,
    )


def normalize_transcript_segments(payload: Mapping[str, Any]) -> List[TranscriptSegment]:
    segments = payload.get("segments") or []
    return [normalize_segment(segment) for segment in segments if isinstance(segment, Mapping)]


def normalize_transcript_words(payload: Mapping[str, Any]) -> List[TranscriptWord]:
    words = payload.get("words") or []
    return [normalize_word(word) for word in words if isinstance(word, Mapping)]


def transcript_text_from_segments(segments: Iterable[Union[TranscriptSegment, Mapping[str, Any]]]) -> str:
    texts: List[str] = []
    for segment in segments:
        if isinstance(segment, TranscriptSegment):
            texts.append(segment.text)
        elif isinstance(segment, Mapping):
            text = segment.get("text")
            if text is not None:
                texts.append(str(text))
    return " ".join(texts).strip()
