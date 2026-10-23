from typing import Dict, Any, Optional
from pydantic import BaseModel


class SummarizationRequest(BaseModel):
    text: str
    max_tokens: Optional[int] = 150
    model: str = "mistral-tiny"
    temperature: float = 0.3


class SummarizationResponse(BaseModel):
    summary: str
    model: str
    input_tokens: int
    output_tokens: int


class ExtractionRequest(BaseModel):
    text: str
    schema: Dict[str, Any]
    model: str = "mistral-small"
    temperature: float = 0.2


class ExtractionResponse(BaseModel):
    extracted_data: Dict[str, Any]
    model: str
    input_tokens: int
    output_tokens: int


class QuestionAnsweringRequest(BaseModel):
    question: str
    context: str
    max_tokens: Optional[int] = 300
    model: str = "mistral-small"
    temperature: float = 0.3


class QuestionAnsweringResponse(BaseModel):
    answer: str
    model: str
    input_tokens: int
    output_tokens: int


class StreamingRequest(BaseModel):
    prompt: str
    model: str = "mistral-tiny"
    max_tokens: Optional[int] = 100
    temperature: float = 0.7


class StreamingChunk(BaseModel):
    text: str
    model: str