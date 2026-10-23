from typing import Any, Dict, Optional, Iterator
from pydantic import BaseModel


class ModelRequest(BaseModel):
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 1000


class ModelResponse(BaseModel):
    output: str
    raw_response: Any


class StreamChunk(BaseModel):
    content: str
    raw_chunk: Any


class ModelResponseWithMetadata(BaseModel):
    output: str
    metadata: Dict[str, Any]
    raw_response: Any