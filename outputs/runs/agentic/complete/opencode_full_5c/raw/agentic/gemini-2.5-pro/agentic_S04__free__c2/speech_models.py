from pydantic import BaseModel, Field
from typing import List, Optional, Union


class TranscriptionRequest(BaseModel):
    audio_url: str
    speaker_labels: bool = False
    punctuate: bool = True
    format_text: bool = True


class TranscriptionWord(BaseModel):
    start: int
    end: int
    text: str
    confidence: float


class TranscriptionUtterance(BaseModel):
    start: int
    end: int
    text: str
    speaker: str
    confidence: float
    words: List[TranscriptionWord]


class TranscriptionResponse(BaseModel):
    id: str
    status: str
    text: Optional[str] = None
    words: Optional[List[TranscriptionWord]] = None
    utterances: Optional[List[TranscriptionUtterance]] = None
    error: Optional[str] = None


class TranslationRequest(BaseModel):
    q: Union[str, List[str]]
    target: str
    source: Optional[str] = None


class Translation(BaseModel):
    translatedText: str
    detectedSourceLanguage: Optional[str] = None


class TranslationResponse(BaseModel):
    translations: List[Translation]


class ModerationRequest(BaseModel):
    input: str
    model: str = "text-moderation-latest"


class ModerationCategory(BaseModel):
    category: str
    score: float
    flagged: bool


class ModerationResult(BaseModel):
    categories: List[ModerationCategory]
    flagged: bool


class ModerationResponse(BaseModel):
    id: str
    model: str
    results: List[ModerationResult]


class SummaryRequest(BaseModel):
    text: str
    model: str = "summarize-xlarge"
    length: str = "medium"
    format: str = "paragraph"
    temperature: float = 0.3


class SummaryResponse(BaseModel):
    id: str
    summary: str


class EmbeddingRequest(BaseModel):
    inputs: List[str]
    model: str = "sentence-transformers/all-MiniLM-L6-v2"


class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]
