from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class TranscriptionStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class WordInfo:
    text: str
    start_ms: int
    end_ms: int
    confidence: float
    speaker: Optional[str] = None


@dataclass
class UtteranceInfo:
    text: str
    speaker: Optional[str]
    start_ms: int
    end_ms: int
    words: list[WordInfo] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class TranscriptionResult:
    transcription_id: str
    status: TranscriptionStatus
    text: str = ""
    utterances: list[UtteranceInfo] = field(default_factory=list)
    words: list[WordInfo] = field(default_factory=list)
    audio_duration_ms: int = 0
    confidence: float = 0.0
    error_message: Optional[str] = None


def normalize_assemblyai_response(raw: dict) -> TranscriptionResult:
    status_map = {
        "queued": TranscriptionStatus.QUEUED,
        "processing": TranscriptionStatus.PROCESSING,
        "completed": TranscriptionStatus.COMPLETED,
        "error": TranscriptionStatus.ERROR,
    }
    status = status_map.get(raw.get("status", "error"), TranscriptionStatus.ERROR)

    words = []
    for w in raw.get("words", []):
        words.append(
            WordInfo(
                text=w.get("text", ""),
                start_ms=w.get("start", 0),
                end_ms=w.get("end", 0),
                confidence=w.get("confidence", 0.0),
                speaker=str(w["speaker"])
                if "speaker" in w and w["speaker"] is not None
                else None,
            )
        )

    utterances = []
    for u in raw.get("utterances", []):
        utterance_words = []
        if "words" in u:
            for w in u["words"]:
                utterance_words.append(
                    WordInfo(
                        text=w.get("text", ""),
                        start_ms=w.get("start", 0),
                        end_ms=w.get("end", 0),
                        confidence=w.get("confidence", 0.0),
                        speaker=str(u.get("speaker"))
                        if u.get("speaker") is not None
                        else None,
                    )
                )
        utterances.append(
            UtteranceInfo(
                text=u.get("text", ""),
                speaker=str(u.get("speaker")) if u.get("speaker") is not None else None,
                start_ms=u.get("start", 0),
                end_ms=u.get("end", 0),
                words=utterance_words,
                confidence=u.get("confidence", 0.0),
            )
        )

    return TranscriptionResult(
        transcription_id=raw.get("id", ""),
        status=status,
        text=raw.get("text", ""),
        utterances=utterances,
        words=words,
        audio_duration_ms=raw.get("audio_duration", 0),
        confidence=raw.get("confidence", 0.0),
        error_message=raw.get("error"),
    )


def normalize_poll_response(raw: dict) -> TranscriptionResult:
    return normalize_assemblyai_response(raw)


def extract_segments_for_translation(result: TranscriptionResult) -> list[dict]:
    segments = []
    if result.utterances:
        for i, utt in enumerate(result.utterances):
            segments.append(
                {
                    "segment_id": i,
                    "speaker": utt.speaker,
                    "text": utt.text,
                    "start_ms": utt.start_ms,
                    "end_ms": utt.end_ms,
                }
            )
    else:
        segments.append(
            {
                "segment_id": 0,
                "speaker": None,
                "text": result.text,
                "start_ms": 0,
                "end_ms": result.audio_duration_ms,
            }
        )
    return segments
