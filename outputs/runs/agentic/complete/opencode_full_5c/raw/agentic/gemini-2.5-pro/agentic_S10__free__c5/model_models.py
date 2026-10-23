from pydantic import BaseModel
from typing import List, Optional


class CompletionRequest(BaseModel):
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 150


class CompletionResponse(BaseModel):
    text: str
    finish_reason: Optional[str] = None


class ModelFamily(BaseModel):
    name: str
    models: List[str]
