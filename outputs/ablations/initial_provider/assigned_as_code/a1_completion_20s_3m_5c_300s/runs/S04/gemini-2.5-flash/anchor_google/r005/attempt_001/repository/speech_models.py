import dataclasses
from typing import List, Optional

@dataclasses.dataclass
class TranscriptionRequest:
    audio_uri: str
    language_code: str
    enable_speaker_diarization: Optional[bool] = False
    enable_word_time_offsets: Optional[bool] = False

@dataclasses.dataclass
class TranscriptionJob:
    job_id: str
    status: str
    transcript: Optional[str] = None
    word_timestamps: Optional[List[dict]] = None
    diarized_transcript: Optional[List[dict]] = None

@dataclasses.dataclass
class TranslationRequest:
    text: str
    target_language_code: str
    source_language_code: Optional[str] = None

@dataclasses.dataclass
class TranslationResult:
    translated_text: str
    detected_language_code: Optional[str] = None

@dataclasses.dataclass
class ModerationRequest:
    text: str

@dataclasses.dataclass
class ModerationResult:
    is_safe: bool
    scores: dict

@dataclasses.dataclass
class SummarizationRequest:
    text: str
    max_output_tokens: Optional[int] = 500

@dataclasses.dataclass
class SummarizationResult:
    summary: str

@dataclasses.dataclass
class EmbeddingRequest:
    text_segments: List[str]

@dataclasses.dataclass
class EmbeddingResult:
    embeddings: List[List[float]]
