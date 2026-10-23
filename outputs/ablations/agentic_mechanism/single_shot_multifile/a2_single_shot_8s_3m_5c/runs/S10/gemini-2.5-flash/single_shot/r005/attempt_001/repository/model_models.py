from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Generator

@dataclass
class TextGenerationInput:
    prompt: str
    model_name: str = "gpt-4o-mini"
    max_tokens: int = 500
    temperature: float = 0.7

@dataclass
class TextGenerationOutput:
    generated_text: str
    model_name: str
    finish_reason: Optional[str] = None

@dataclass
class JsonExtractionInput:
    text: str
    json_schema: Dict[str, Any]
    model_name: str = "gpt-4o-mini"
    temperature: float = 0.0

@dataclass
class JsonExtractionOutput:
    extracted_json: Dict[str, Any]
    model_name: str
    finish_reason: Optional[str] = None

@dataclass
class ContextAnswerInput:
    question: str
    context: str
    model_name: str = "gpt-4o-mini"
    max_tokens: int = 200
    temperature: float = 0.2

@dataclass
class ContextAnswerOutput:
    answer: str
    model_name: str
    finish_reason: Optional[str] = None

@dataclass
class StreamCompletionInput:
    prompt: str
    model_name: str = "gpt-4o-mini"
    max_tokens: int = 500
    temperature: float = 0.7

@dataclass
class StreamCompletionOutputChunk:
    token: str
    finish_reason: Optional[str] = None

@dataclass
class EmbeddingInput:
    text: str
    model_name: str = "text-embedding-3-small"

@dataclass
class EmbeddingOutput:
    embedding: List[float]
    model_name: str