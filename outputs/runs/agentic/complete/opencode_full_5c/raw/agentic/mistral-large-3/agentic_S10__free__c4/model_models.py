from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class SummarizationRequest(BaseModel):
    input_text: str
    max_tokens: int = 150
    temperature: float = 0.3
    model: Optional[str] = "mistral/mistral-large-latest"


class SummarizationResponse(BaseModel):
    summary: str


class ExtractionRequest(BaseModel):
    input_text: str
    json_schema: Dict[str, Any]
    max_tokens: int = 250
    temperature: float = 0.2
    model: Optional[str] = "mistral/mistral-large-latest"


class ExtractionResponse(BaseModel):
    extracted_data: Dict[str, Any]


class QARequest(BaseModel):
    question: str
    context: str
    max_tokens: int = 300
    temperature: float = 0.5
    model: Optional[str] = "mistral/mistral-large-latest"


class QAResponse(BaseModel):
    answer: str


class CompletionRequest(BaseModel):
    prompt: str
    max_tokens: int = 100
    temperature: float = 0.7
    model: Optional[str] = "mistral/mistral-large-latest"
    stream: bool = False


class CompletionResponse(BaseModel):
    completion: str
