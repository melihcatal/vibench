from typing import List, Optional
from pydantic import BaseModel

class TranscriptionJob(BaseModel):
    job_id: str
    status: str
    audio_url: str

class WordTimestamp(BaseModel):
    text: str
    start: int
    end: int

class DiarizedSegment(BaseModel):
    speaker: str
    text: str
    start: int
    end: int

class TranscriptionResult(BaseModel):
    job_id: str
    transcript_text: str
    words: Optional[List[WordTimestamp]] = None
    diarized_segments: Optional[List[DiarizedSegment]] = None

class TranslationRequest(BaseModel):
    text: str
    target_language: str # e.g., "DE" for German, "FR" for French

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    detected_source_language: str

class ModerationResult(BaseModel):
    text: str
    is_flagged: bool
    categories: dict

class SummaryResult(BaseModel):
    original_text: str
    summary: str

class EmbeddingResult(BaseModel):
    texts: List[str]
    embeddings: List[List[float]]
    model: str
