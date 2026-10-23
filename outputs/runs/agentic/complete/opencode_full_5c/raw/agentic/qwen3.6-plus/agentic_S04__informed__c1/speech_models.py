from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class WordInfo:
    text: str
    start_ms: int
    end_ms: int
    confidence: float
    speaker: Optional[str] = None


@dataclass
class UtteranceInfo:
    speaker: str
    text: str
    start_ms: int
    end_ms: int
    confidence: float
    words: List[WordInfo] = field(default_factory=list)


@dataclass
class TranscriptionResult:
    job_id: str
    status: str
    text: str = ""
    confidence: float = 0.0
    utterances: List[UtteranceInfo] = field(default_factory=list)
    words: List[WordInfo] = field(default_factory=list)
    audio_duration_ms: Optional[int] = None
    error: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class TranscriptionSubmission:
    job_id: str
    status: str
    audio_url: str = ""
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class TranscriptSegment:
    index: int
    speaker: str
    text: str
    start_ms: int
    end_ms: int


@dataclass
class TranscriptSegments:
    segments: List[TranscriptSegment]
    total_segments: int
    audio_duration_ms: Optional[int] = None


def normalize_utterances(raw_utterances: List[Dict[str, Any]]) -> List[UtteranceInfo]:
    utterances = []
    for u in raw_utterances:
        words = [
            WordInfo(
                text=w["text"],
                start_ms=w["start"],
                end_ms=w["end"],
                confidence=w.get("confidence", 0.0),
                speaker=u.get("speaker"),
            )
            for w in u.get("words", [])
        ]
        utterances.append(
            UtteranceInfo(
                speaker=u.get("speaker", "unknown"),
                text=u["text"],
                start_ms=u["start"],
                end_ms=u["end"],
                confidence=u.get("confidence", 0.0),
                words=words,
            )
        )
    return utterances


def normalize_words(raw_words: List[Dict[str, Any]]) -> List[WordInfo]:
    return [
        WordInfo(
            text=w["text"],
            start_ms=w["start"],
            end_ms=w["end"],
            confidence=w.get("confidence", 0.0),
            speaker=w.get("speaker"),
        )
        for w in raw_words
    ]


def parse_transcription_result(raw: Dict[str, Any]) -> TranscriptionResult:
    status = raw.get("status", "unknown")
    error = raw.get("error")
    utterances = normalize_utterances(raw.get("utterances", []))
    words = normalize_words(raw.get("words", []))
    text = raw.get("text", "")
    confidence = raw.get("confidence", 0.0)
    audio_duration_ms = raw.get("audio_duration")

    return TranscriptionResult(
        job_id=raw.get("id", ""),
        status=status,
        text=text,
        confidence=confidence,
        utterances=utterances,
        words=words,
        audio_duration_ms=audio_duration_ms,
        error=error,
        raw_response=raw,
    )


def result_to_segments(result: TranscriptionResult) -> TranscriptSegments:
    segments = []
    for i, u in enumerate(result.utterances):
        segments.append(
            TranscriptSegment(
                index=i,
                speaker=u.speaker,
                text=u.text,
                start_ms=u.start_ms,
                end_ms=u.end_ms,
            )
        )
    return TranscriptSegments(
        segments=segments,
        total_segments=len(segments),
        audio_duration_ms=result.audio_duration_ms,
    )
