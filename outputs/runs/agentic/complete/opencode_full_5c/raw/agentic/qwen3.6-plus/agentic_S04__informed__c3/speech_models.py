from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TranscriptionRequest:
    audio_url: str
    speaker_labels: bool = False
    word_boost: Optional[list[str]] = None
    custom_spelling: Optional[list[dict]] = None
    language_code: Optional[str] = None
    auto_highlights: bool = False
    content_safety: bool = False
    iab_categories: bool = False
    extra_config: Optional[dict] = None


@dataclass
class WordSegment:
    text: str
    start: int
    end: int
    confidence: float
    speaker: Optional[str] = None


@dataclass
class Utterance:
    speaker: str
    text: str
    start: int
    end: int
    words: list[WordSegment] = field(default_factory=list)
    confidence: float = 1.0


@dataclass
class TranscriptionResult:
    transcript_id: str
    status: str
    text: str
    words: list[WordSegment] = field(default_factory=list)
    utterances: list[Utterance] = field(default_factory=list)
    confidence: float = 0.0
    audio_duration: float = 0.0
    language_code: Optional[str] = None
    error: Optional[str] = None


@dataclass
class TranscriptSummary:
    transcript_id: str
    summary_text: str
    key_topics: list[str] = field(default_factory=list)
    sentiment: Optional[str] = None


def normalize_word(raw_word: dict) -> WordSegment:
    return WordSegment(
        text=raw_word["text"],
        start=raw_word["start"],
        end=raw_word["end"],
        confidence=raw_word.get("confidence", 0.0),
        speaker=raw_word.get("speaker"),
    )


def normalize_utterance(raw_utterance: dict) -> Utterance:
    words = [normalize_word(w) for w in raw_utterance.get("words", [])]
    return Utterance(
        speaker=raw_utterance.get("speaker", "Unknown"),
        text=raw_utterance.get("text", ""),
        start=raw_utterance.get("start", 0),
        end=raw_utterance.get("end", 0),
        words=words,
        confidence=raw_utterance.get("confidence", 1.0),
    )


def normalize_transcription_response(response: dict) -> TranscriptionResult:
    status = response.get("status", "unknown")
    error = response.get("error")
    words = [normalize_word(w) for w in response.get("words", [])]
    utterances = [normalize_utterance(u) for u in response.get("utterances", [])]
    return TranscriptionResult(
        transcript_id=response.get("id", ""),
        status=status,
        text=response.get("text", ""),
        words=words,
        utterances=utterances,
        confidence=response.get("confidence", 0.0),
        audio_duration=response.get("audio_duration", 0.0) / 1000.0
        if response.get("audio_duration")
        else 0.0,
        language_code=response.get("language_code"),
        error=error,
    )


def extract_segments_with_timestamps(result: TranscriptionResult) -> list[dict]:
    segments = []
    for word in result.words:
        segments.append(
            {
                "text": word.text,
                "start_ms": word.start,
                "end_ms": word.end,
                "speaker": word.speaker,
                "confidence": word.confidence,
            }
        )
    return segments


def extract_diarized_utterances(result: TranscriptionResult) -> list[dict]:
    return [
        {
            "speaker": u.speaker,
            "text": u.text,
            "start_ms": u.start,
            "end_ms": u.end,
            "confidence": u.confidence,
        }
        for u in result.utterances
    ]
