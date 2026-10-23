import dataclasses
from typing import Optional, List, Dict, Any

@dataclasses.dataclass
class TranscriptionJobRequest:
    audio_file_uri: str
    job_name: str
    language_code: str = "en-US"
    enable_speaker_diarization: bool = False
    max_speakers: int = 2 # for diarization
    output_bucket_name: Optional[str] = None # AWS Transcribe needs an S3 bucket for output
    output_key: Optional[str] = None # Path in S3 bucket

@dataclasses.dataclass
class TranscriptionJobStatus:
    job_name: str
    status: str # e.g., IN_PROGRESS, COMPLETED, FAILED
    transcript_file_uri: Optional[str] = None
    failure_reason: Optional[str] = None

@dataclasses.dataclass
class TranscriptWord:
    word: str
    start_time: float
    end_time: float
    speaker_label: Optional[str] = None

@dataclasses.dataclass
class TranscriptSegment:
    start_time: float
    end_time: float
    speaker_label: Optional[str] = None
    text: str
    words: List[TranscriptWord]

@dataclasses.dataclass
class TranscriptionResult:
    job_name: str
    language_code: str
    transcript_text: str
    segments: List[TranscriptSegment]
    raw_output: Dict[str, Any] # Store the full JSON output

@dataclasses.dataclass
class TranslatedSegment:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str

@dataclasses.dataclass
class ModerationResult:
    original_text: str
    is_profane: bool
    review_recommended: bool
    terms: List[str] # List of flagged terms

@dataclasses.dataclass
class SummaryResult:
    original_text: str
    summary_text: str
    model_used: str

@dataclasses.dataclass
class EmbeddingResult:
    original_text: str
    embedding: List[float]
    model_used: str
