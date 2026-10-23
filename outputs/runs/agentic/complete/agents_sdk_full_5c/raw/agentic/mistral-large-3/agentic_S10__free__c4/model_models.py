from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from openai.types.chat import ChatCompletion


class SummarizationRequest(BaseModel):
    input_text: str
    max_tokens: Optional[int] = 150
    temperature: Optional[float] = 0.3
    model: Optional[str] = "gpt-4o-mini"


class SummarizationResponse(BaseModel):
    summary: str

    @classmethod
    def from_openai(cls, response: ChatCompletion) -> "SummarizationResponse":
        return cls(summary=response.choices[0].message.content)


class ExtractionRequest(BaseModel):
    input_text: str
    schema: Dict[str, Any]
    model: Optional[str] = "gpt-4o-mini"


class ExtractionResponse(BaseModel):
    extracted_data: Dict[str, Any]

    @classmethod
    def from_openai(cls, response: ChatCompletion) -> "ExtractionResponse":
        import json
        content = response.choices[0].message.content
        return cls(extracted_data=json.loads(content))


class QARequest(BaseModel):
    question: str
    context: str
    max_tokens: Optional[int] = 150
    model: Optional[str] = "gpt-4o-mini"


class QAResponse(BaseModel):
    answer: str

    @classmethod
    def from_openai(cls, response: ChatCompletion) -> "QAResponse":
        return cls(answer=response.choices[0].message.content)


class CompletionRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 100
    temperature: Optional[float] = 0.7
    model: Optional[str] = "gpt-4o-mini"