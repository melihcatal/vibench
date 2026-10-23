from pydantic import BaseModel
from typing import Dict, Any, Optional, List


class SummarizationRequest(BaseModel):
    input_text: str
    max_tokens: int = 150
    temperature: float = 0.3
    model: str = "meta-llama/Meta-Llama-3-8B-Instruct"


class SummarizationResponse(BaseModel):
    summary: str


class ExtractionRequest(BaseModel):
    input_text: str
    schema: Dict[str, Any]
    model: str = "mistralai/Mistral-7B-Instruct-v0.2"


class ExtractionResponse(BaseModel):
    extracted_json: str


class QARequest(BaseModel):
    question: str
    context: str
    max_tokens: int = 300
    temperature: float = 0.5
    model: str = "meta-llama/Meta-Llama-3-8B-Instruct"


class QAResponse(BaseModel):
    answer: str


class CompletionRequest(BaseModel):
    prompt: str
    max_tokens: int = 100
    temperature: float = 0.7
    model: str = "meta-llama/Meta-Llama-3-8B-Instruct"
    stream: bool = False


class CompletionChunk(BaseModel):
    text: str