from typing import Dict, Any, Optional
from pydantic import BaseModel


class SummarizationRequest(BaseModel):
    model_id: str
    input: str
    parameters: Dict[str, Any]


class SummarizationResponse(BaseModel):
    output: str

    @classmethod
    def from_watsonx(cls, response: Any) -> "SummarizationResponse":
        return cls(output=response.result.results[0].generated_text)


class ExtractionRequest(BaseModel):
    model_id: str
    input: str
    parameters: Dict[str, Any]


class ExtractionResponse(BaseModel):
    output: str

    @classmethod
    def from_watsonx(cls, response: Any) -> "ExtractionResponse":
        return cls(output=response.result.results[0].generated_text)


class ContextualAnswerRequest(BaseModel):
    model_id: str
    input: str
    parameters: Dict[str, Any]


class ContextualAnswerResponse(BaseModel):
    output: str

    @classmethod
    def from_watsonx(cls, response: Any) -> "ContextualAnswerResponse":
        return cls(output=response.result.results[0].generated_text)


class StreamCompletionRequest(BaseModel):
    model_id: str
    input: str
    parameters: Dict[str, Any]


class StreamCompletionChunk(BaseModel):
    output: str

    @classmethod
    def from_watsonx(cls, chunk: Any) -> "StreamCompletionChunk":
        return cls(output=chunk.result.results[0].generated_text)