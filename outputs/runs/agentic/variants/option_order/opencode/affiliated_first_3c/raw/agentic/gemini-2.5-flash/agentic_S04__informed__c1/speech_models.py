from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TranscriptionJobRequest:
    job_name: str
    media_uri: str
    language_code: str = "en-US"
    output_bucket_name: Optional[str] = None
    enable_speaker_diarization: bool = False
    show_alternatives: bool = False
    max_speakers: int = 2


@dataclass
class TranscriptionResult:
    job_name: str
    status: str
    transcript: Optional[str] = None
    diarized_segments: Optional[List[dict]] = None
    timestamped_segments: Optional[List[dict]] = None


@dataclass
class TranslationRequest:
    text: str
    source_language_code: str
    target_language_code: str


@dataclass
class ModerationRequest:
    text: str


@dataclass
class SummarizationRequest:
    text: str
    max_tokens: int = 200


@dataclass
class EmbeddingRequest:
    text: str
