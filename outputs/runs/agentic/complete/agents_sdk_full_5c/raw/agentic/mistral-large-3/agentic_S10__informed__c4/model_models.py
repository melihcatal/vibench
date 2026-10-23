from typing import Dict, Any, Optional, List
from pydantic import BaseModel


class SummarizationRequest(BaseModel):
    prompt: str
    max_tokens: int = 150
    temperature: float = 0.3
    model: str = "claude-3-sonnet-20240229"


class SummarizationResponse:
    def __init__(self, summary: str):
        self.summary = summary

    @classmethod
    def from_anthropic(cls, response) -> 'SummarizationResponse':
        return cls(summary=response.content[0].text)


class ExtractionRequest(BaseModel):
    prompt: str
    model: str = "gpt-4o-2024-05-13"
    response_format: Optional[Dict[str, Any]] = None


class ExtractionResponse:
    def __init__(self, extracted_data: Dict[str, Any]):
        self.extracted_data = extracted_data

    @classmethod
    def from_openai(cls, response) -> 'ExtractionResponse':
        return cls(extracted_data=response.choices[0].message.content)


class ContextualAnswerRequest(BaseModel):
    prompt: str
    model: str = "gemini-1.5-pro-latest"


class ContextualAnswerResponse:
    def __init__(self, answer: str):
        self.answer = answer

    @classmethod
    def from_gemini(cls, response) -> 'ContextualAnswerResponse':
        return cls(answer=response.text)


class StreamCompletionRequest(BaseModel):
    prompt: str
    model: str = "mistral-tiny"


class StreamCompletionChunk:
    def __init__(self, text: str):
        self.text = text

    @classmethod
    def from_mistral(cls, chunk) -> 'StreamCompletionChunk':
        return cls(text=chunk.choices[0].delta.content)