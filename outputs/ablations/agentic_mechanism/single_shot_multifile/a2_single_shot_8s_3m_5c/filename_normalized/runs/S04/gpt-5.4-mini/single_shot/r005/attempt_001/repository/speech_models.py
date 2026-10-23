from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SubmitTranscriptionRequest:
    audio_file_path: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SubmitTranscriptionResponse:
    job_id: str
    status: str
    transcript: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {"job_id": self.job_id, "status": self.status, "transcript": self.transcript}


@dataclass
class PollTranscriptionResponse:
    job_id: str
    status: str
    transcript: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {"job_id": self.job_id, "status": self.status, "transcript": self.transcript}


@dataclass
class DiarizedTranscriptRequest:
    audio_file_path: str
    speaker_count: Optional[int] = None


@dataclass
class TimestampedTranscriptRequest:
    audio_file_path: str
    granularity: str = "word"


@dataclass
class TranslateTranscriptRequest:
    transcript: Dict[str, Any]
    target_language: str


@dataclass
class ModerateTranscriptRequest:
    transcript_text: str


@dataclass
class ArchiveSummaryRequest:
    transcript: Dict[str, Any]


@dataclass
class TranscriptEmbeddingRequest:
    segments: List[str]


def normalize_transcription_result(result: Any) -> Dict[str, Any]:
    if isinstance(result, dict):
        return result
    if hasattr(result, "model_dump"):
        return result.model_dump()
    if hasattr(result, "dict"):
        return result.dict()
    return {"text": str(result)}
