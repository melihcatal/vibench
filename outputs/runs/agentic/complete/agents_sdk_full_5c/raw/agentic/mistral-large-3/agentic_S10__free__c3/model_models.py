from pydantic import BaseModel
from typing import Dict, Any, Optional

class SummarizationRequest(BaseModel):
    model: str
    text: str
    max_length: Optional[int] = 150

class SummarizationResponse(BaseModel):
    summary: str

class ExtractionRequest(BaseModel):
    model: str
    text: str
    schema: Dict[str, Any]

class ExtractionResponse(BaseModel):
    extracted_json: str

class QARequest(BaseModel):
    model: str
    question: str
    context: str
    max_tokens: Optional[int] = 100

class QAResponse(BaseModel):
    answer: str

class CompletionRequest(BaseModel):
    model: str
    prompt: str
    max_tokens: int
    stream: bool = False

class CompletionChunk(BaseModel):
    text: str