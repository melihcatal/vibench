from typing import Dict, Any, Optional
from pydantic import BaseModel


class SummarizationRequest(BaseModel):
    text: str
    max_length: Optional[int] = 150
    model: str = "anthropic.claude-3-sonnet-20240229-v1:0"


class SummarizationResponse(BaseModel):
    summary: str

    @classmethod
    def from_anthropic(cls, response: Any) -> "SummarizationResponse":
        return cls(summary=response.content[0].text)


class ExtractionRequest(BaseModel):
    text: str
    schema: Dict[str, Any]
    model: str = "anthropic.claude-3-haiku-20240307-v1:0"


class ExtractionResponse(BaseModel):
    extracted_data: Dict[str, Any]

    @classmethod
    def from_anthropic(cls, response: Any) -> "ExtractionResponse":
        import json
        content = response.content[0].text
        try:
            data = json.loads(content)
            return cls(extracted_data=data)
        except json.JSONDecodeError:
            return cls(extracted_data={"error": "Failed to parse JSON"})


class QARequest(BaseModel):
    question: str
    context: str
    model: str = "anthropic.claude-3-opus-20240229-v1:0"


class QAResponse(BaseModel):
    answer: str

    @classmethod
    def from_anthropic(cls, response: Any) -> "QAResponse":
        return cls(answer=response.content[0].text)


class CompletionRequest(BaseModel):
    prompt: str
    model: str = "anthropic.claude-3-sonnet-20240229-v1:0"


class CompletionChunk(BaseModel):
    text: str