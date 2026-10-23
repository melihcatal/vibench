from pydantic import BaseModel
from typing import Optional

class TranscriptChunk(BaseModel):
    """
    Represents a single chunk of a transcript, which can be partial or final.
    """
    text: str
    is_final: bool
    timestamp_ms: int

class TranslationResponse(BaseModel):
    """

    Represents a translated text response.
    """
    original_text: str
    translated_text: str
    target_language: str

class SafetyAnalysisResult(BaseModel):
    """
    Represents the result of a content safety check.
    """
    is_safe: bool
    flags: Optional[dict] = None

class SummaryResponse(BaseModel):
    """
    Represents a summarized text response.
    """
    original_text: str
    summary_text: str

class EmbeddingResponse(BaseModel):
    """
    Represents an embedding vector for a text chunk.
    """
    text: str
    embedding: list[float]
