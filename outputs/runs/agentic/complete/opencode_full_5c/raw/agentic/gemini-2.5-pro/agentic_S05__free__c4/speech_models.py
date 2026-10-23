from typing import List, Optional
from pydantic import BaseModel, Field


class StreamingRecognitionResult(BaseModel):
    transcript: str
    is_final: bool
    stability: float


class TranslationResponse(BaseModel):
    translated_text: str
    detected_language_code: Optional[str] = None


class ContentSafetyResponse(BaseModel):
    toxicity_score: float = Field(
        ...,
        description="Value from 0 to 1 representing the likelihood of toxicity.",
    )


class SummaryResponse(BaseModel):
    summary: str


class EmbeddingResponse(BaseModel):
    embedding: List[float]
