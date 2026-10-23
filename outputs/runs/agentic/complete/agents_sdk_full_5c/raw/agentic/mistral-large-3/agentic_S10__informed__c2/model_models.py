from typing import Dict, Any, Optional
from pydantic import BaseModel


class SummarizationRequest(BaseModel):
    model: str
    prompt: str
    temperature: float


class ExtractionRequest(BaseModel):
    model: str
    prompt: str
    temperature: float


class ContextualAnswerRequest(BaseModel):
    model: str
    prompt: str
    temperature: float


class StreamingRequest(BaseModel):
    model: str
    prompt: str
    temperature: float


class SummarizationResponse(BaseModel):
    output: str


class ExtractionResponse(BaseModel):
    output: str


class ContextualAnswerResponse(BaseModel):
    output: str


class StreamingResponseChunk(BaseModel):
    token: str