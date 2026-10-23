from typing import TypedDict, List, Dict


class BatchTranscriptionRequest(TypedDict):
    audio_path: str
    language: str
    diarization: bool
    timestamps: bool


class TranscriptionJobStatus(TypedDict):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"


class TranscriptionSegment(TypedDict):
    start: float
    end: float
    text: str
    speaker_label: str | None = None


class TranscriptResult(TypedDict):
    jobId: str
    status: str
    segments: List[TranscriptionSegment]


class TranslationSegment(TypedDict):
    start: float
    end: float
    text: str
    target_language: str
