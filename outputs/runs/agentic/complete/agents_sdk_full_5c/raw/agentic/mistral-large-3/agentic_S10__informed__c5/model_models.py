from typing import Dict, Any, Optional
from pydantic import BaseModel


class SummarizationRequest(BaseModel):
    text: str
    model_id: str
    temperature: float = 0.7
    max_tokens: int = 150
    extra_params: Dict[str, Any] = {}


class SummarizationResponse(BaseModel):
    summary: str


class ExtractionRequest(BaseModel):
    text: str
    schema: Dict[str, Any]
    model_id: str
    temperature: float = 0.3
    extra_params: Dict[str, Any] = {}


class ExtractionResponse(BaseModel):
    json_data: str


class QARequest(BaseModel):
    question: str
    context: str
    model_id: str
    temperature: float = 0.7
    max_tokens: int = 150
    extra_params: Dict[str, Any] = {}


class QAResponse(BaseModel):
    answer: str


class CompletionRequest(BaseModel):
    prompt: str
    model_id: str
    temperature: float = 0.7
    max_tokens: int = 150
    extra_params: Dict[str, Any] = {}


class CompletionChunk(BaseModel):
    text: str