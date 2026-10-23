from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class TranscriptionRequest:
    job_name: str
    media_uri: str
    media_format: str
    language_code: str
    output_bucket: str
    diarization_enabled: bool = False
    show_speaker_labels: bool = False
    show_alternatives: bool = False
    max_speakers: int = 2

@dataclass
class TranscriptionJobStatus:
    job_name: str
    status: str
    transcript_file_uri: Optional[str] = None
    failure_reason: Optional[str] = None

@dataclass
class TranscriptionResult:
    job_name: str
    status: str
    transcript_text: Optional[str] = None
    word_timestamps: Optional[List[Dict[str, Any]]] = None
    segments: Optional[List[Dict[str, Any]]] = None
    speaker_labels: Optional[List[Dict[str, Any]]] = None

@dataclass
class TranslatedSegment:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str

@dataclass
class ModerationResult:
    text: str
    moderation_labels: List[Dict[str, Any]]

@dataclass
class SummaryResult:
    original_text: str
    summary_text: str

@dataclass
class EmbeddingResult:
    segment_text: str
    embedding: List[float]
