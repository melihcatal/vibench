from typing import Dict, Any, Optional
from pydantic import BaseModel


class SummarizationRequest(BaseModel):
    text: str
    max_tokens: int = 150
    temperature: float = 0.3


class SummarizationResponse(BaseModel):
    summary: str
    tokens_used: int


class ExtractionRequest(BaseModel):
    text: str
    schema: Dict[str, Any]
    max_tokens: int = 500
    temperature: float = 0.2


class ExtractionResponse(BaseModel):
    extracted_data: Dict[str, Any]
    tokens_used: int


class QARequest(BaseModel):
    question: str
    context: str
    max_tokens: int = 500
    temperature: float = 0.5


class QAResponse(BaseModel):
    answer: str
    tokens_used: int


def normalize_model_response(response: Any) -> Dict[str, Any]:
    if hasattr(response, "choices") and response.choices:
        return {
            "content": response.choices[0].message.content.strip(),
            "tokens_used": response.usage.total_tokens
            if hasattr(response, "usage")
            else 0,
        }
    return {"content": "", "tokens_used": 0}
