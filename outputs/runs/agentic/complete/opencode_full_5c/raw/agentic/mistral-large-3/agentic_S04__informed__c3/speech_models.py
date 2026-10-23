from typing import Optional, List, Dict
from pydantic import BaseModel


class TranscriptionJobRequest(BaseModel):
    job_name: str
    media_uri: str
    language_code: str
    media_format: str
    output_bucket: Optional[str] = None
    show_speaker_labels: bool = False
    max_speaker_labels: Optional[int] = None
    channel_identification: bool = False


class TranscriptionJobResponse(BaseModel):
    job_name: str
    job_status: str
    job_id: str


class TranscriptSegment(BaseModel):
    start_time: float
    end_time: float
    speaker_label: Optional[str] = None
    text: str


class DiarizedTranscriptResponse(BaseModel):
    segments: List[TranscriptSegment]


class TimestampedTranscriptResponse(BaseModel):
    words: List[Dict[str, float]]
    segments: List[TranscriptSegment]


class TranslationRequest(BaseModel):
    text: str
    source_language: str
    target_language: str


class TranslationResponse(BaseModel):
    translated_text: str


class ModerationRequest(BaseModel):
    text: str


class ModerationResponse(BaseModel):
    is_flagged: bool
    flagged_categories: List[str]
    scores: Dict[str, float]


class SummaryRequest(BaseModel):
    text: str
    max_length: Optional[int] = 100


class SummaryResponse(BaseModel):
    summary: str


class EmbeddingRequest(BaseModel):
    texts: List[str]


class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]
