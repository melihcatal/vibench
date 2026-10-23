from typing import Optional, Dict, Any, Iterator
from pydantic import BaseModel


class LLMRequest(BaseModel):
    """Request model for LLM inference."""

    model_family: str
    model_id: str
    prompt: str
    max_tokens: int = 1000
    temperature: float = 0.7
    stream: bool = False


class LLMResponse(BaseModel):
    """Response model for LLM inference."""

    text: str

    class Config:
        arbitrary_types_allowed = True
