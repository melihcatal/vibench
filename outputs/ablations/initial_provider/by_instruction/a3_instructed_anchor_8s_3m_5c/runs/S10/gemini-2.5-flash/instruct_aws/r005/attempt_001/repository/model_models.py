from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class LLMRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 500
    temperature: Optional[float] = 0.7
    stop_sequences: Optional[List[str]] = None

class LLMResponse(BaseModel):
    generated_text: str
    raw_response: Dict[str, Any]

class SummaryRequest(LLMRequest):
    pass

class SummaryResponse(LLMResponse):
    pass

class JsonExtractionRequest(LLMRequest):
    schema: Dict[str, Any]

class JsonExtractionResponse(LLMResponse):
    extracted_json: Dict[str, Any]

class AnswerWithContextRequest(LLMRequest):
    question: str
    context: str

class AnswerWithContextResponse(LLMResponse):
    pass

class StreamCompletionRequest(LLMRequest):
    pass

# Add more models for other functionalities like safety, translation, embedding, etc.
