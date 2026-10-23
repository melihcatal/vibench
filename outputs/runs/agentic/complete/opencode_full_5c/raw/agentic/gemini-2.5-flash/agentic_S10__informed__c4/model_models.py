import dataclasses
from typing import Optional, Dict, Any, List


@dataclasses.dataclass
class LLMRequest:
    prompt: str
    model_name: str = "gemini-pro"
    temperature: float = 0.7
    max_output_tokens: Optional[int] = None


@dataclasses.dataclass
class LLMResponse:
    text: str


@dataclasses.dataclass
class SummarizeRequest(LLMRequest):
    pass


@dataclasses.dataclass
class ExtractJsonRequest(LLMRequest):
    json_schema: Dict[str, Any]


@dataclasses.dataclass
class AnswerWithContextRequest(LLMRequest):
    context: str
    question: str


@dataclasses.dataclass
class StreamCompletionRequest(LLMRequest):
    pass


@dataclasses.dataclass
class EmbeddingRequest:
    text: str
    model_name: str = "models/embedding-001"


@dataclasses.dataclass
class EmbeddingResponse:
    embedding: List[float]
