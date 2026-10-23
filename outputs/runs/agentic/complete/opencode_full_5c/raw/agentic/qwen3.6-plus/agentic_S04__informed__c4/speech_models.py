from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class TranscriptionStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class TranscriptionRequest:
    audio_url: str
    language_code: str = "en"
    speaker_labels: bool = False
    word_timestamps: bool = False
    model: str = "assemblyai/nano-2"
    custom_spelling: Optional[list] = None
    auto_highlights: bool = False
    content_safety: bool = False


@dataclass
class TranscriptionJob:
    job_id: str
    status: TranscriptionStatus
    audio_url: str
    created_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None


@dataclass
class WordTimestamp:
    word: str
    start_ms: int
    end_ms: int
    confidence: float
    speaker: Optional[str] = None


@dataclass
class Utterance:
    text: str
    start_ms: int
    end_ms: int
    speaker: Optional[str] = None
    words: list = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class TranscriptionResult:
    job_id: str
    status: TranscriptionStatus
    text: str
    utterances: list = field(default_factory=list)
    words: list = field(default_factory=list)
    language_code: str = "en"
    audio_duration_ms: int = 0
    confidence: float = 0.0


@dataclass
class TranslationRequest:
    segments: list
    target_language: str = "en"
    source_language: Optional[str] = None


@dataclass
class TranslationResult:
    segments: list
    target_language: str
    source_language: str


@dataclass
class ModerationRequest:
    text: str
    categories: Optional[list] = None


@dataclass
class ModerationResult:
    text: str
    flagged: bool
    categories: dict = field(default_factory=dict)
    confidence_scores: dict = field(default_factory=dict)


@dataclass
class SummaryRequest:
    text: str
    summary_type: str = "paragraph"
    max_length: int = 200


@dataclass
class SummaryResult:
    text: str
    summary_type: str
    word_count: int = 0


@dataclass
class EmbeddingRequest:
    segments: list
    model: str = "text-embedding-3-small"


@dataclass
class EmbeddingResult:
    segments: list
    embeddings: list
    model: str


def normalize_assemblyai_response(raw_response: dict) -> TranscriptionResult:
    utterances = []
    words = []

    if raw_response.get("utterances"):
        for utt in raw_response["utterances"]:
            utterances.append(
                Utterance(
                    text=utt.get("text", ""),
                    start_ms=int(utt.get("start", 0) * 1000),
                    end_ms=int(utt.get("end", 0) * 1000),
                    speaker=utt.get("speaker"),
                    confidence=utt.get("confidence", 0.0),
                )
            )

    if raw_response.get("words"):
        for w in raw_response["words"]:
            words.append(
                WordTimestamp(
                    word=w.get("text", ""),
                    start_ms=int(w.get("start", 0) * 1000),
                    end_ms=int(w.get("end", 0) * 1000),
                    confidence=w.get("confidence", 0.0),
                )
            )

    return TranscriptionResult(
        job_id=raw_response.get("id", ""),
        status=TranscriptionStatus(raw_response.get("status", "failed")),
        text=raw_response.get("text", ""),
        utterances=utterances,
        words=words,
        language_code=raw_response.get("language_code", "en"),
        audio_duration_ms=int(raw_response.get("audio_duration", 0) * 1000),
        confidence=raw_response.get("confidence", 0.0),
    )


def normalize_deepl_translation(
    raw_segments: list, raw_response: list, target_lang: str, source_lang: str
) -> TranslationResult:
    translated = []
    for seg, resp in zip(raw_segments, raw_response):
        translated.append(
            {
                "original": seg,
                "translated": resp.get("text", ""),
                "detected_source": resp.get("detected_source_language", source_lang),
            }
        )
    return TranslationResult(
        segments=translated,
        target_language=target_lang,
        source_language=source_lang,
    )


def normalize_tisane_moderation(raw_response: dict, text: str) -> ModerationResult:
    categories = {}
    confidence_scores = {}
    flagged = False

    if "violence" in raw_response:
        categories["violence"] = raw_response["violence"].get("detected", False)
        confidence_scores["violence"] = raw_response["violence"].get("confidence", 0.0)
        if categories["violence"]:
            flagged = True

    if "sexual" in raw_response:
        categories["sexual"] = raw_response["sexual"].get("detected", False)
        confidence_scores["sexual"] = raw_response["sexual"].get("confidence", 0.0)
        if categories["sexual"]:
            flagged = True

    if "hate" in raw_response:
        categories["hate"] = raw_response["hate"].get("detected", False)
        confidence_scores["hate"] = raw_response["hate"].get("confidence", 0.0)
        if categories["hate"]:
            flagged = True

    return ModerationResult(
        text=text,
        flagged=flagged,
        categories=categories,
        confidence_scores=confidence_scores,
    )
