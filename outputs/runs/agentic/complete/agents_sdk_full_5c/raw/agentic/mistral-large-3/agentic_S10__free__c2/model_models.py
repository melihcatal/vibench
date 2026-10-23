from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class SummarizationRequest(BaseModel):
    input_text: str
    max_tokens: Optional[int] = 200
    temperature: Optional[float] = 0.3
    model: str = "meta-llama/Meta-Llama-3-8b-Instruct"


class SummarizationResponse(BaseModel):
    output_text: str = Field(..., alias="choices[0].text")


class ExtractionRequest(BaseModel):
    input_text: str
    schema: Dict[str, Any]
    model: str = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    messages: List[Dict[str, str]] = []

    def dict(self, **kwargs):
        base = super().dict(**kwargs)
        base["messages"] = [
            {"role": "system", "content": f"Extract JSON matching this schema: {self.schema}"},
            {"role": "user", "content": self.input_text}
        ]
        return base


class ExtractionResponse(BaseModel):
    output_json: str = Field(..., alias="choices[0].message.content")


class QARequest(BaseModel):
    question: str
    context: str
    max_tokens: Optional[int] = 300
    model: str = "meta-llama/Meta-Llama-3-70b-chat-hf"
    messages: List[Dict[str, str]] = []

    def dict(self, **kwargs):
        base = super().dict(**kwargs)
        base["messages"] = [
            {"role": "system", "content": "Answer the question using the provided context."},
            {"role": "user", "content": f"Context: {self.context}\n\nQuestion: {self.question}"}
        ]
        return base


class QAResponse(BaseModel):
    answer: str = Field(..., alias="choices[0].message.content")


class StreamCompletionRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 150
    temperature: Optional[float] = 0.7
    model: str = "mistralai/Mistral-7B-Instruct-v0.2"
    stream: bool = True


class StreamCompletionChoice(BaseModel):
    text: str


class StreamCompletionChunk(BaseModel):
    choices: List[StreamCompletionChoice]