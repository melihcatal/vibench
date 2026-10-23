from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptionRequest:
    audio_url: str
    language_code: Optional[str] = None
    speaker_labels: bool = False
    speakers_expected: Optional[int] = None


@dataclass
class TranscriptionJob:
    transcript_id: str
    status: str
    audio_url: Optional[str] = None


@dataclass
class TranscriptSegment:
    text: str
    start: Optional[int] = None
    end: Optional[int] = None
    speaker: Optional[str] = None
    confidence: Optional[float] = None
    words: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class TranscriptResult:
    transcript_id: str
    status: str
    text: str
    language_code: Optional[str] = None
    confidence: Optional[float] = None
    segments: List[TranscriptSegment] = field(default_factory=list)
    utterances: List[TranscriptSegment] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


def _normalize_words(words: Optional[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for item in words or []:
        normalized.append(
            {
                "text": item.get("text") or item.get("word") or "",
                "start": item.get("start"),
                "end": item.get("end"),
                "confidence": item.get("confidence"),
                "speaker": item.get("speaker"),
            }
        )
    return normalized


def normalize_assemblyai_transcript(payload: Any) -> TranscriptResult:
    transcript_id = getattr(payload, "id", None) or payload.get("id")
    status = getattr(payload, "status", None) or payload.get("status") or "unknown"
    text = getattr(payload, "text", None) or payload.get("text") or ""
    language_code = getattr(payload, "language_code", None) or payload.get(
        "language_code"
    )
    confidence = getattr(payload, "confidence", None) or payload.get("confidence")
    raw = payload if isinstance(payload, dict) else payload.__dict__.copy()

    utterance_items = (
        getattr(payload, "utterances", None)
        if not isinstance(payload, dict)
        else payload.get("utterances")
    )
    word_items = (
        getattr(payload, "words", None)
        if not isinstance(payload, dict)
        else payload.get("words")
    )

    utterances: List[TranscriptSegment] = []
    for item in utterance_items or []:
        source = item if isinstance(item, dict) else item.__dict__
        utterances.append(
            TranscriptSegment(
                text=source.get("text", ""),
                start=source.get("start"),
                end=source.get("end"),
                speaker=source.get("speaker"),
                confidence=source.get("confidence"),
                words=_normalize_words(source.get("words")),
            )
        )

    segments: List[TranscriptSegment] = []
    if utterances:
        segments = utterances
    elif word_items:
        for item in word_items:
            source = item if isinstance(item, dict) else item.__dict__
            segments.append(
                TranscriptSegment(
                    text=source.get("text") or source.get("word") or "",
                    start=source.get("start"),
                    end=source.get("end"),
                    speaker=source.get("speaker"),
                    confidence=source.get("confidence"),
                    words=[
                        {
                            "text": source.get("text") or source.get("word") or "",
                            "start": source.get("start"),
                            "end": source.get("end"),
                            "confidence": source.get("confidence"),
                            "speaker": source.get("speaker"),
                        }
                    ],
                )
            )

    return TranscriptResult(
        transcript_id=transcript_id,
        status=status,
        text=text,
        language_code=language_code,
        confidence=confidence,
        segments=segments,
        utterances=utterances,
        raw=raw,
    )


def transcript_to_publishable_text(result: TranscriptResult) -> str:
    if result.utterances:
        return "\n".join(
            f"{segment.speaker or 'speaker'}: {segment.text}"
            for segment in result.utterances
            if segment.text
        )
    if result.segments:
        return "\n".join(segment.text for segment in result.segments if segment.text)
    return result.text
