from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class ModelRequest(BaseModel):
    messages: List[Message]
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None


class Choice(BaseModel):
    index: int
    message: Message
    finish_reason: Optional[str] = None


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ModelResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Usage


class StreamResponseChunk(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Dict[str, Any]]


class ModelResponseWithMetadata(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Usage
    metadata: Dict[str, Any]


class SafetyCheckRequest(BaseModel):
    text: str


class SafetyCheckResponse(BaseModel):
    is_safe: bool
    categories: Dict[str, bool]
    scores: Dict[str, float]


class TranslationRequest(BaseModel):
    text: str
    target_language: str
    source_language: Optional[str] = None


class TranslationResponse(BaseModel):
    translated_text: str
    detected_language: Optional[str] = None


class EmbeddingRequest(BaseModel):
    texts: List[str]


class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]
    model: str


class AudioRequest(BaseModel):
    text: str
    voice: Optional[str] = None
    format: Optional[str] = "mp3"


class AudioResponse(BaseModel):
    audio_content: bytes
    format: str
