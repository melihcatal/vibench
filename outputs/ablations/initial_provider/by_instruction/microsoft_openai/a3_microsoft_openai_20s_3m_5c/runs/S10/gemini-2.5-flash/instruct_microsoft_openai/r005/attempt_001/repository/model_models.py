from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class LLMRequest(BaseModel):
    prompt: str
    model: str = "gpt-3.5-turbo"
    max_tokens: Optional[int] = 150
    temperature: Optional[float] = 0.7

class LLMResponseChoice(BaseModel):
    text: str
    index: int
    finish_reason: Optional[str]

class LLMResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[LLMResponseChoice]

class SummaryRequest(LLMRequest):
    pass

class SummaryResponse(LLMResponse):
    pass

class JsonExtractionRequest(LLMRequest):
    json_schema: Dict[str, Any]

class JsonExtractionResponse(LLMResponse):
    extracted_json: Dict[str, Any]

class QuestionAnsweringRequest(LLMRequest):
    context: str
    question: str

class QuestionAnsweringResponse(LLMResponse):
    answer: str

class StreamCompletionRequest(LLMRequest):
    pass

class StreamCompletionChunk(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Dict[str, Any]] # Simplified for streaming chunks
