from dataclasses import dataclass
from typing import Optional, Dict, Any, List


@dataclass
class LLMRequest:
    prompt: str
    model: str
    max_tokens: int = 1024
    temperature: float = 0.7


@dataclass
class LLMResponse:
    generated_text: str
    finish_reason: Optional[str] = None


@dataclass
class ExtractionRequest:
    text: str
    schema: Dict[str, Any]
    model: str = "gpt-4-turbo-preview"


@dataclass
class ExtractionResponse:
    extracted_json: Dict[str, Any]


@dataclass
class ContextAnswerRequest:
    question: str
    context: str
    model: str


@dataclass
class StreamCompletionRequest:
    prompt: str
    model: str
    max_tokens: int = 1024
    temperature: float = 0.7
