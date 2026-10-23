from typing import TypedDict, List


class TranscriptionRequest(TypedDict):
    """Payload for submitting batch transcription."""

    file_path: str
    language: str
    # optional provider-specific hints
    # e.g., {"dia": True} for diarization
    settings: dict | None = None


class TranscriptionResponse(TypedDict):
    """Successful response from batch transcription API."""

    job_id: str
    status: str  # e.g., \"IN_PROGRESS\" or \"COMPLETED\"
    # optional: preview segment or transcript fragment


class TimestampResponse(TypedDict):
    """Response containing word or segment timestamps."""

    timestamps: List[dict]
    # each entry: {\"start\": float, \"end\": float, \"word\": str, ...}


class DiarizationResponse(TypedDict):
    """Response with speaker labels."""

    diarized_text: str
    speakers: List[str]


class TranslationRequest(TypedDict):
    """Payload for translation of completed transcript segments."""

    text: str
    source_lang: str
    target_lang: str


class TranslationResponse(TypedDict):
    translated_text: str
    detected_source_language: str | None


class ModerationRequest(TypedDict):
    """Payload for content moderation of transcripts."""

    text: str
    language: str


class ModerationResponse(TypedDict):
    """Moderation outcome."""

    safe: bool
    flagged_categories: list[str] | None
    content: str  # cleaned/transcribed version


class SummaryRequest(TypedDict):
    """Payload to summarize a transcript."""

    transcript: str


class SummaryResponse(TypedDict):
    summary: str
    highlights: list[str]


class EmbeddingRequest(TypedDict):
    """Payload to embed transcript segments."""

    text: str
    model: str | None = None


class EmbeddingResponse(TypedDict):
    embedding: list[float]
    model: str
