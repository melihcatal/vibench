from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class InferenceRequest(BaseModel):
    prompt: str
    max_output_tokens: int = 1024
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 40


class InferenceResponse(BaseModel):
    generated_text: str
    safety_attributes: Optional[Dict[str, Any]] = None


class ContextualInferenceRequest(InferenceRequest):
    context: str
    question: str


class TranslationRequest(BaseModel):
    text: str
    target_language_code: str
    source_language_code: Optional[str] = None


class TranslationResponse(BaseModel):
    translated_text: str


class EmbeddingRequest(BaseModel):
    text: List[str]


class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]


class SpeechRequest(BaseModel):
    text: str
    language_code: str = "en-US"
    voice_name: str = "en-US-Standard-A"
    speaking_rate: float = 1.0
    pitch: float = 0.0


class SpeechResponse(BaseModel):
    audio_content: bytes
