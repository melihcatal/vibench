from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class TranscriptionStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"


class PollResult(str, Enum):
    SUCCESS = "success"
    STILL_PROCESSING = "still_processing"
    FAILED = "failed"


@dataclass
class TranscriptionRequest:
    audio_url: str
    language_code: str = "en"
    audio_format: str = "mp3"
    speaker_labels: bool = False
    word_timestamps: bool = False
    custom_spelling: Optional[list] = None
    content_safety: bool = False
    auto_chapters: bool = False
    punctuate: bool = True
    format_text: bool = True
    dual_channel: bool = False
    webhook_url: Optional[str] = None
    metadata: Optional[dict] = None


@dataclass
class TranscriptionSubmissionResult:
    job_id: str
    audio_url: str
    status: TranscriptionStatus
    submitted_at: Optional[str] = None


@dataclass
class WordSegment:
    text: str
    start_ms: int
    end_ms: int
    confidence: float
    speaker: Optional[str] = None


@dataclass
class UtteranceSegment:
    text: str
    speaker: Optional[str] = None
    start_ms: int = 0
    end_ms: int = 0
    words: list = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class TranscriptionResult:
    job_id: str
    status: TranscriptionStatus
    text: str = ""
    utterances: list = field(default_factory=list)
    words: list = field(default_factory=list)
    audio_duration_ms: int = 0
    language: str = ""
    confidence: float = 0.0
    error_message: Optional[str] = None


@dataclass
class PollResultData:
    result: PollResult
    status: TranscriptionStatus
    job_id: str
    transcription: Optional[TranscriptionResult] = None
    error_message: Optional[str] = None


@dataclass
class TranslationSegment:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    speaker: Optional[str] = None


@dataclass
class TranslationResult:
    segments: list = field(default_factory=list)
    source_language: str = ""
    target_language: str = ""


@dataclass
class ModerationCategory:
    name: str
    score: float
    severity: str = "unknown"


@dataclass
class ModerationResult:
    text: str
    flagged: bool = False
    categories: list = field(default_factory=list)
    overall_severity: str = "safe"


@dataclass
class SummaryResult:
    summary: str
    key_topics: list = field(default_factory=list)
    action_items: list = field(default_factory=list)
    sentiment: str = "neutral"


@dataclass
class EmbeddingSegment:
    text: str
    embedding: list = field(default_factory=list)
    speaker: Optional[str] = None
    segment_index: int = 0


@dataclass
class EmbeddingResult:
    segments: list = field(default_factory=list)
    model: str = ""
    dimensions: int = 0


def normalize_assemblyai_response(
    raw_response: dict, job_id: str
) -> TranscriptionResult:
    status_map = {
        "queued": TranscriptionStatus.QUEUED,
        "processing": TranscriptionStatus.PROCESSING,
        "completed": TranscriptionStatus.COMPLETED,
        "error": TranscriptionStatus.ERROR,
    }
    status = status_map.get(
        raw_response.get("status", "error"), TranscriptionStatus.ERROR
    )
    error_message = raw_response.get("error")
    utterances = []
    for utt in raw_response.get("utterances", []):
        words = [
            WordSegment(
                text=w.get("text", ""),
                start_ms=w.get("start", 0),
                end_ms=w.get("end", 0),
                confidence=w.get("confidence", 0.0),
                speaker=utt.get("speaker"),
            )
            for w in utt.get("words", [])
        ]
        utterances.append(
            UtteranceSegment(
                text=utt.get("text", ""),
                speaker=utt.get("speaker"),
                start_ms=utt.get("start", 0),
                end_ms=utt.get("end", 0),
                words=words,
                confidence=utt.get("confidence", 0.0),
            )
        )
    words_list = [
        WordSegment(
            text=w.get("text", ""),
            start_ms=w.get("start", 0),
            end_ms=w.get("end", 0),
            confidence=w.get("confidence", 0.0),
        )
        for w in raw_response.get("words", [])
    ]
    return TranscriptionResult(
        job_id=job_id,
        status=status,
        text=raw_response.get("text", ""),
        utterances=utterances,
        words=words_list,
        audio_duration_ms=raw_response.get("audio_duration", 0) * 1000
        if raw_response.get("audio_duration")
        else 0,
        language=raw_response.get("language_code", ""),
        confidence=raw_response.get("confidence", 0.0),
        error_message=error_message,
    )


def normalize_deepl_response(
    raw_translations: list, source_lang: str, target_lang: str
) -> TranslationResult:
    segments = []
    for item in raw_translations:
        segments.append(
            TranslationSegment(
                original_text=item.get("original_text", ""),
                translated_text=item.get("translated_text", ""),
                source_language=source_lang,
                target_language=target_lang,
            )
        )
    return TranslationResult(
        segments=segments,
        source_language=source_lang,
        target_language=target_lang,
    )


def normalize_azure_safety_response(raw_response: dict, text: str) -> ModerationResult:
    categories = []
    flagged = False
    max_severity = 0.0
    severity_labels = {0: "safe", 1: "low", 2: "medium", 3: "high", 4: "critical"}
    for cat_result in raw_response.get("categoriesAnalysis", []):
        cat_name = cat_result.get("category", "Unknown")
        severity = cat_result.get("severity", 0)
        if severity > max_severity:
            max_severity = severity
        if cat_result.get("safeResult") == "Unsafe":
            flagged = True
        categories.append(
            ModerationCategory(
                name=cat_name,
                score=cat_result.get("severity", 0),
                severity=severity_labels.get(severity, "unknown"),
            )
        )
    return ModerationResult(
        text=text,
        flagged=flagged,
        categories=categories,
        overall_severity=severity_labels.get(int(max_severity), "safe"),
    )


def normalize_dashscope_summary(raw_response: dict) -> SummaryResult:
    output_text = ""
    if raw_response.get("output") and raw_response["output"].get("text"):
        output_text = raw_response["output"]["text"]
    return SummaryResult(
        summary=output_text,
        key_topics=[],
        action_items=[],
        sentiment="neutral",
    )


def normalize_dashscope_embedding(raw_response: dict, model: str) -> EmbeddingResult:
    segments = []
    output = raw_response.get("output", {})
    embeddings_data = output.get("embeddings", [])
    for idx, emb_item in enumerate(embeddings_data):
        segments.append(
            EmbeddingSegment(
                text=emb_item.get("text", ""),
                embedding=emb_item.get("embedding", []),
                segment_index=idx,
            )
        )
    return EmbeddingResult(
        segments=segments,
        model=model,
        dimensions=len(segments[0].embedding) if segments else 0,
    )
