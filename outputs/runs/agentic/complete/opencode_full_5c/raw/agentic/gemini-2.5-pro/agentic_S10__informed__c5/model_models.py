from dataclasses import dataclass
from typing import List, Dict


@dataclass
class CompletionRequest:
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 1024


@dataclass
class CompletionResponse:
    text: str


@dataclass
class JsonExtractionRequest:
    text_content: str
    json_schema: Dict


@dataclass
class JsonExtractionResponse:
    json_data: Dict


@dataclass
class ContextualAnswerRequest:
    context: str
    question: str


@dataclass
class ContextualAnswerResponse:
    answer: str


@dataclass
class StreamCompletionRequest:
    prompt: str


@dataclass
class EmbeddingRequest:
    texts: List[str]


@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]
