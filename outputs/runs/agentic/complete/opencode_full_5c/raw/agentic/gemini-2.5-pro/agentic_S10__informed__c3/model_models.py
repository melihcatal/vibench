from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class Message(BaseModel):
    role: str
    content: str


class CompletionRequest(BaseModel):
    messages: List[Message]
    model: str = "gpt-4o"
    max_tokens: int = 1024
    temperature: float = 0.7
    stream: bool = False


class CompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Dict[str, Any]]
    usage: Optional[Dict[str, int]] = None


class SafetyResult(BaseModel):
    category: str
    severity: int


class TranslationResponse(BaseModel):
    detected_source_language: str
    text: str


class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]
