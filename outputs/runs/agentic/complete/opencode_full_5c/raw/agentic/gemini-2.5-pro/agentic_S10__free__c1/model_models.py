from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class ModelConfig(BaseModel):
    api_key: str = Field(..., env="COHERE_API_KEY")


class SummarizeRequest(BaseModel):
    text: str
    length: str = "medium"
    format: str = "paragraph"
    model: str = "command"
    extractiveness: str = "low"
    temperature: float = 0.3


class SummarizeResponse(BaseModel):
    summary: str
    meta: Optional[Dict[str, Any]] = None


class ExtractJsonRequest(BaseModel):
    text: str
    model: str = "command-r"


class ExtractJsonResponse(BaseModel):
    json_output: Dict[str, Any]


class AnswerWithContextRequest(BaseModel):
    question: str
    context: str
    model: str = "command-r"


class AnswerWithContextResponse(BaseModel):
    answer: str


class StreamCompletionRequest(BaseModel):
    prompt: str
    model: str = "command-r"


class EmbeddingRequest(BaseModel):
    texts: List[str]
    model: str = "embed-english-v3.0"
    input_type: str = "search_document"


class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]
