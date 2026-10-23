from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class ModelInvocationRequest(BaseModel):
    prompt: str
    max_tokens: int = 512
    temperature: float = 0.8
    model_id: str

class ModelInvocationResponse(BaseModel):
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    finish_reason: Optional[str] = None

class EmbeddingRequest(BaseModel):
    texts: List[str]
    model: str = "embed-english-v3.0"
    input_type: str = "search_document"

class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]
    meta: Optional[Dict[str, Any]] = None

class SafetyAnalysis(BaseModel):
    is_safe: bool
    categories: Dict[str, int]

class TranslationRequest(BaseModel):
    text: str
    target_language: str = "DE" # German

class TranslationResponse(BaseModel):
    translated_text: str
    detected_source_language: str

class AudioGenerationRequest(BaseModel):
    text: str
    voice_id: str = "21m00Tcm4TlvDq8ikWAM" # Pre-selected voice from ElevenLabs
    model_id: str = "eleven_multilingual_v2"
