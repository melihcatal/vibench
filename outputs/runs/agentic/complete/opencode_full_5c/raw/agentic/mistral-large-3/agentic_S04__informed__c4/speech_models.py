from typing import Optional, List, Dict
from pydantic import BaseModel


class TranscriptionRequest(BaseModel):
    audio_url: str
    language_code: Optional[str] = "en"
    enable_speaker_diarization: Optional[bool] = False
    enable_word_timestamps: Optional[bool] = False


class TranscriptionResponse(BaseModel):
    transcription_id: str
    text: Optional[str] = None
    status: str
    words: Optional[List[Dict]] = None
    utterances: Optional[List[Dict]] = None


class DiarizedTranscriptResponse(BaseModel):
    transcription_id: str
    utterances: List[Dict]


class TimestampedTranscriptResponse(BaseModel):
    transcription_id: str
    words: List[Dict]


class TranslationRequest(BaseModel):
    text: str
    target_language: str


class TranslationResponse(BaseModel):
    translated_text: str


class ModerationRequest(BaseModel):
    text: str


class ModerationResponse(BaseModel):
    flagged: bool
    categories: Dict[str, bool]
    scores: Dict[str, float]


class SummaryRequest(BaseModel):
    text: str
    max_length: Optional[int] = 150


class SummaryResponse(BaseModel):
    summary: str


class EmbeddingRequest(BaseModel):
    text: str


class EmbeddingResponse(BaseModel):
    embedding: List[float]
