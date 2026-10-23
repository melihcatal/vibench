from typing import Any, Dict, List, Generator
from pydantic import BaseModel

class CompletionRequest(BaseModel):
    prompt: str
    model_name: str = "default"

class CompletionResponse(BaseModel):
    text: str
    provider_response: Any = None

class ModerationRequest(BaseModel):
    text: str

class ModerationResponse(BaseModel):
    is_unsafe: bool
    categories: Dict[str, Any] = {}

class TranslationRequest(BaseModel):
    text: str
    target_language_code: str

class TranslationResponse(BaseModel):
    translated_text: str

class EmbeddingRequest(BaseModel):
    texts: List[str]

class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]

class AudioRequest(BaseModel):
    text: str
    voice_id: str = "Joanna"
    output_format: str = "mp3"