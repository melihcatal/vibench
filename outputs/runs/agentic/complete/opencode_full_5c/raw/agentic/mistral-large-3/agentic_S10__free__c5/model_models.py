from typing import Dict, Any, Optional
from pydantic import BaseModel


class SummarizationRequest(BaseModel):
    model: str
    text: str
    max_tokens: int
    temperature: float
    system_prompt: str


class SummarizationResponse(BaseModel):
    summary: str
    model: str
    usage: Dict[str, int]


class ExtractionRequest(BaseModel):
    model: str
    text: str
    max_tokens: int
    temperature: float
    system_prompt: str


class ExtractionResponse(BaseModel):
    extracted_json: Dict[str, Any]
    model: str
    usage: Dict[str, int]


class QARequest(BaseModel):
    model: str
    question: str
    context: str
    max_tokens: int
    temperature: float
    system_prompt: str


class QAResponse(BaseModel):
    answer: str
    model: str
    usage: Dict[str, int]


class CompletionRequest(BaseModel):
    model: str
    prompt: str
    max_tokens: int
    temperature: float
    stream: bool = False


class CompletionResponse(BaseModel):
    delta: str
    model: str
