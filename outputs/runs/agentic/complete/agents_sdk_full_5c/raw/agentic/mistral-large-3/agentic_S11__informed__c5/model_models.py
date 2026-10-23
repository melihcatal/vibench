from typing import Dict, Any, Optional, Iterator
from pydantic import BaseModel

class PlatformRequest(BaseModel):
    prompt: str
    max_tokens: int = 1000
    temperature: float = 0.9

class PlatformResponse(BaseModel):
    output: str
    metadata: Dict[str, Any]

class PlatformStreamChunk(BaseModel):
    chunk: str
    metadata: Dict[str, Any]